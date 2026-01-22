#!/usr/bin/env python3
"""
Dicționar Român pentru Kobo eReader
Extrage doar definiții COMPLETE din DEX '98 și DEX '96
"""

import mysql.connector
import re
from collections import defaultdict
import sys

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'dexonline',
    'charset': 'utf8mb4',
    'use_unicode': True
}

# Surse cu definiții complete (verificat în baza de date)
SOURCES_WITH_DEFINITIONS = (1, 2)  # DEX '98, DEX '96

def clean_definition(text):
    """Curăță markup-ul intern DEX și returnează HTML curat."""
    if not text:
        return ""
    
    result = text
    
    # @ ... @ -> bold (cuvânt principal)
    result = re.sub(r'@([^@]+)@', r'<b>\1</b>', result)
    
    # # ... # -> italic (abrevieri gramaticale)
    result = re.sub(r'#([^#]+)#', r'<i>\1</i>', result)
    
    # $ ... $ -> italic (exemple)
    result = re.sub(r'\$([^$]+)\$', r'<i>\1</i>', result)
    
    # ^n sau ^{text} -> superscript
    result = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', result)
    result = re.sub(r'\^(\d+)', r'<sup>\1</sup>', result)
    result = re.sub(r'\^([A-Za-z])', r'<sup>\1</sup>', result)
    
    # Curățăm caractere rămase
    result = result.replace('@', '')
    result = result.replace('#', '')
    result = result.replace('$', '')
    result = result.replace('%', '')
    
    # Normalizăm spațiile
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def main():
    print("=== Dicționar Român pentru Kobo ===", file=sys.stderr)
    print("Conectare la MySQL...", file=sys.stderr)
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True, buffered=True)
    
    # ===== PASUL 1: Extrage definiții complete din DEX '98 și DEX '96 =====
    print("\n[1/3] Extragere definiții din DEX '98 și DEX '96...", file=sys.stderr)
    
    query_definitions = """
    SELECT 
        l.id as lexeme_id,
        l.formNoAccent as lemma,
        l.description as word_info,
        d.id as definition_id,
        d.internalRep as definition,
        s.shortName as source_name
    FROM Lexeme l
    JOIN EntryLexeme el ON el.lexemeId = l.id
    JOIN EntryDefinition ed ON ed.entryId = el.entryId
    JOIN Definition d ON d.id = ed.definitionId
    JOIN Source s ON s.id = d.sourceId
    WHERE d.status = 0
      AND d.sourceId IN (1, 2)
      AND LENGTH(d.internalRep) > 50
    ORDER BY l.formNoAccent, l.id, d.sourceId, d.id
    """
    
    cursor.execute(query_definitions)
    
    lexeme_data = {}
    lexeme_definitions = defaultdict(list)
    
    row_count = 0
    for row in cursor:
        row_count += 1
        if row_count % 10000 == 0:
            print(f"  Procesate {row_count} definiții...", file=sys.stderr)
        
        lexeme_id = row['lexeme_id']
        definition_id = row['definition_id']
        
        if lexeme_id not in lexeme_data:
            lexeme_data[lexeme_id] = {
                'lemma': row['lemma'],
                'word_info': row['word_info'] or '',
                'seen_defs': set()
            }
        
        # Evităm duplicatele
        if definition_id not in lexeme_data[lexeme_id]['seen_defs']:
            lexeme_data[lexeme_id]['seen_defs'].add(definition_id)
            source = row['source_name']
            definition = row['definition']
            lexeme_definitions[lexeme_id].append((definition, source))
    
    print(f"  ✓ {len(lexeme_data)} cuvinte cu definiții complete", file=sys.stderr)
    
    # ===== PASUL 2: Extrage forme flexionate =====
    print("\n[2/3] Extragere forme flexionate...", file=sys.stderr)
    
    query_inflected = """
    SELECT lexemeId, formNoAccent as form
    FROM InflectedForm
    WHERE lexemeId IN (
        SELECT DISTINCT l.id
        FROM Lexeme l
        JOIN EntryLexeme el ON el.lexemeId = l.id
        JOIN EntryDefinition ed ON ed.entryId = el.entryId
        JOIN Definition d ON d.id = ed.definitionId
        WHERE d.status = 0 AND d.sourceId IN (1, 2) AND LENGTH(d.internalRep) > 50
    )
    ORDER BY lexemeId, formNoAccent
    """
    
    cursor.execute(query_inflected)
    
    lexeme_variants = defaultdict(set)
    row_count = 0
    for row in cursor:
        row_count += 1
        if row_count % 100000 == 0:
            print(f"  Procesate {row_count} forme...", file=sys.stderr)
        
        lexeme_variants[row['lexemeId']].add(row['form'])
    
    print(f"  ✓ {row_count} forme flexionate", file=sys.stderr)
    
    cursor.close()
    conn.close()
    
    # ===== PASUL 3: Generare fișier .df =====
    print("\n[3/3] Generare fișier dicthtml...", file=sys.stderr)
    
    output_file = '/Users/cld/Desktop/DEX/dex-ro.df'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        processed = 0
        
        for lexeme_id, definitions in lexeme_definitions.items():
            data = lexeme_data[lexeme_id]
            lemma = data['lemma']
            word_info = data['word_info']
            variants = lexeme_variants.get(lexeme_id, set())
            
            if not lemma or not definitions:
                continue
            
            # @ Headword
            f.write(f"@ {lemma}\n")
            
            # & Variante (forme flexionate pentru lookup)
            for variant in sorted(variants):
                if variant and variant != lemma:
                    f.write(f"& {variant}\n")
            
            # : Info gramatical (opțional)
            if word_info:
                f.write(f": {word_info}\n")
            
            # Definiții
            all_defs = []
            for i, (defn, source) in enumerate(definitions, 1):
                cleaned = clean_definition(defn)
                if cleaned:
                    if len(definitions) > 1:
                        all_defs.append(f"<p><b>{i}.</b> {cleaned} <small>[{source}]</small></p>")
                    else:
                        all_defs.append(f"<p>{cleaned} <small>[{source}]</small></p>")
            
            f.write('\n'.join(all_defs) + "\n\n")
            
            processed += 1
            if processed % 10000 == 0:
                print(f"  Scrise {processed} intrări...", file=sys.stderr)
    
    print(f"\n✓ Finalizat: {processed} cuvinte cu definiții", file=sys.stderr)
    print(f"  Fișier: {output_file}", file=sys.stderr)

if __name__ == '__main__':
    main()
