#!/usr/bin/env python3
"""
Module de manipulation de texte pour Toolbox
Effectue diverses opérations sur les fichiers texte
"""

import argparse
import sys
from pathlib import Path
import re

VERSION = "1.0.0"
DESCRIPTION = "Manipule et transforme les fichiers texte"

def count_words(text: str) -> dict:
    """Compte les mots, lignes et caractères"""
    lines = text.split('\n')
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(' ', ''))
    
    return {
        'lines': len(lines),
        'words': len(words),
        'characters': chars,
        'characters_no_spaces': chars_no_spaces
    }

def find_replace(text: str, pattern: str, replacement: str, use_regex: bool = False) -> str:
    """Recherche et remplace du texte"""
    if use_regex:
        return re.sub(pattern, replacement, text)
    else:
        return text.replace(pattern, replacement)

def extract_emails(text: str) -> list:
    """Extrait les adresses email du texte"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_urls(text: str) -> list:
    """Extrait les URLs du texte"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

def main(args):
    parser = argparse.ArgumentParser(
        description="Manipulation de fichiers texte",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  toolbox text_tools --count fichier.txt
  toolbox text_tools --replace "ancien" "nouveau" fichier.txt
  toolbox text_tools --extract-emails fichier.txt
        """
    )
    
    parser.add_argument('file', help='Fichier texte à traiter')
    parser.add_argument('--count', action='store_true', help='Compte mots/lignes/caractères')
    parser.add_argument('--replace', nargs=2, metavar=('OLD', 'NEW'), 
                       help='Remplace OLD par NEW')
    parser.add_argument('--regex', action='store_true', 
                       help='Utilise les expressions régulières pour --replace')
    parser.add_argument('--extract-emails', action='store_true', 
                       help='Extrait les adresses email')
    parser.add_argument('--extract-urls', action='store_true', 
                       help='Extrait les URLs')
    parser.add_argument('-o', '--output', help='Fichier de sortie (pour --replace)')
    
    parsed_args = parser.parse_args(args)
    
    # Vérifie que le fichier existe
    if not Path(parsed_args.file).exists():
        print(f"Erreur: Le fichier '{parsed_args.file}' n'existe pas")
        return 1
    
    try:
        # Lit le fichier
        with open(parsed_args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Exécute l'opération demandée
        if parsed_args.count:
            stats = count_words(content)
            print(f"Statistiques pour '{parsed_args.file}':")
            print(f"  Lignes: {stats['lines']}")
            print(f"  Mots: {stats['words']}")
            print(f"  Caractères: {stats['characters']}")
            print(f"  Caractères (sans espaces): {stats['characters_no_spaces']}")
        
        elif parsed_args.replace:
            old_text, new_text = parsed_args.replace
            modified_content = find_replace(content, old_text, new_text, parsed_args.regex)
            
            output_file = parsed_args.output or parsed_args.file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            print(f"Remplacement effectué dans '{output_file}'")
        
        elif parsed_args.extract_emails:
            emails = extract_emails(content)
            if emails:
                print("Adresses email trouvées:")
                for email in sorted(set(emails)):
                    print(f"  {email}")
            else:
                print("Aucune adresse email trouvée")
        
        elif parsed_args.extract_urls:
            urls = extract_urls(content)
            if urls:
                print("URLs trouvées:")
                for url in sorted(set(urls)):
                    print(f"  {url}")
            else:
                print("Aucune URL trouvée")
        
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
