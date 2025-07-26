import re
from typing import List, Tuple, Dict

class PIIDetector:
    """Detects and redacts Personally Identifiable Information (PII) from text"""
    
    def __init__(self):
        # Common first names (subset for detection)
        self.common_first_names = {
            'james', 'mary', 'john', 'patricia', 'robert', 'jennifer', 'michael', 'linda',
            'william', 'elizabeth', 'david', 'barbara', 'richard', 'susan', 'joseph', 'jessica',
            'thomas', 'sarah', 'charles', 'karen', 'christopher', 'nancy', 'daniel', 'lisa',
            'matthew', 'betty', 'anthony', 'helen', 'mark', 'sandra', 'donald', 'donna',
            'steven', 'carol', 'paul', 'ruth', 'andrew', 'sharon', 'joshua', 'michelle',
            'kenneth', 'laura', 'kevin', 'sarah', 'brian', 'kimberly', 'george', 'deborah',
            'timothy', 'dorothy', 'ronald', 'lisa', 'jason', 'nancy', 'edward', 'karen',
            'jeffrey', 'betty', 'ryan', 'helen', 'jacob', 'sandra', 'gary', 'donna',
            'nicholas', 'carol', 'eric', 'ruth', 'jonathan', 'sharon', 'stephen', 'michelle',
            'larry', 'laura', 'justin', 'sarah', 'scott', 'kimberly', 'brandon', 'deborah',
            'benjamin', 'dorothy', 'samuel', 'amy', 'gregory', 'angela', 'alexander', 'ashley',
            'patrick', 'brenda', 'frank', 'emma', 'raymond', 'olivia', 'jack', 'cynthia'
        }
        
        # Common last names (subset for detection)
        self.common_last_names = {
            'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia', 'miller', 'davis',
            'rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez', 'wilson', 'anderson',
            'thomas', 'taylor', 'moore', 'jackson', 'martin', 'lee', 'perez', 'thompson',
            'white', 'harris', 'sanchez', 'clark', 'ramirez', 'lewis', 'robinson', 'walker',
            'young', 'allen', 'king', 'wright', 'scott', 'torres', 'nguyen', 'hill',
            'flores', 'green', 'adams', 'nelson', 'baker', 'hall', 'rivera', 'campbell',
            'mitchell', 'carter', 'roberts', 'gomez', 'phillips', 'evans', 'turner', 'diaz',
            'parker', 'cruz', 'edwards', 'collins', 'reyes', 'stewart', 'morris', 'morales',
            'murphy', 'cook', 'rogers', 'gutierrez', 'ortiz', 'morgan', 'cooper', 'peterson',
            'bailey', 'reed', 'kelly', 'howard', 'ramos', 'kim', 'cox', 'ward', 'richardson',
            'watson', 'brooks', 'chavez', 'wood', 'james', 'bennett', 'gray', 'mendoza'
        }
        
        # Regex patterns for various PII types
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'),
            'ssn': re.compile(r'\b\d{3}-?\d{2}-?\d{4}\b'),
            'date_of_birth': re.compile(r'\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](19|20)\d{2}\b|\b(19|20)\d{2}[/-](0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])\b'),
            'address': re.compile(r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl)\b', re.IGNORECASE),
            'zip_code': re.compile(r'\b\d{5}(-\d{4})?\b')
        }
    
    def detect_names(self, text: str) -> List[Tuple[str, int, int]]:
        """Detect potential names in text"""
        names = []
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        for word in words:
            word_lower = word.lower()
            if word_lower in self.common_first_names or word_lower in self.common_last_names:
                # Find all occurrences of this name in the text
                for match in re.finditer(r'\b' + re.escape(word) + r'\b', text):
                    names.append((word, match.start(), match.end()))
        
        return names
    
    def redact_pii(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Redact PII from text and return both redacted text and list of redactions
        Returns: (redacted_text, redactions_list)
        """
        redacted_text = text
        redactions = []
        
        # Track offset changes due to replacements
        offset = 0
        
        # Store all matches with their positions
        all_matches = []
        
        # Detect emails
        for match in self.patterns['email'].finditer(text):
            all_matches.append(('EMAIL', match.group(), match.start(), match.end()))
        
        # Detect phone numbers
        for match in self.patterns['phone'].finditer(text):
            all_matches.append(('PHONE', match.group(), match.start(), match.end()))
        
        # Detect SSNs
        for match in self.patterns['ssn'].finditer(text):
            all_matches.append(('SSN', match.group(), match.start(), match.end()))
        
        # Detect dates of birth
        for match in self.patterns['date_of_birth'].finditer(text):
            all_matches.append(('DATE_OF_BIRTH', match.group(), match.start(), match.end()))
        
        # Detect addresses
        for match in self.patterns['address'].finditer(text):
            all_matches.append(('ADDRESS', match.group(), match.start(), match.end()))
        
        # Detect zip codes
        for match in self.patterns['zip_code'].finditer(text):
            all_matches.append(('ZIP_CODE', match.group(), match.start(), match.end()))
        
        # Detect names
        name_matches = self.detect_names(text)
        for name, start, end in name_matches:
            all_matches.append(('NAME', name, start, end))
        
        # Sort matches by position (reverse order to maintain positions when replacing)
        all_matches.sort(key=lambda x: x[2], reverse=True)
        
        # Remove overlapping matches (keep the first one found)
        filtered_matches = []
        for match in all_matches:
            pii_type, value, start, end = match
            # Check if this match overlaps with any already accepted match
            overlaps = False
            for existing in filtered_matches:
                _, _, ex_start, ex_end = existing
                if not (end <= ex_start or start >= ex_end):  # Overlaps
                    overlaps = True
                    break
            if not overlaps:
                filtered_matches.append(match)
        
        # Apply redactions
        for pii_type, value, start, end in filtered_matches:
            replacement = f"[REDACTED {pii_type}]"
            redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
            
            redactions.append({
                'type': pii_type,
                'original_value': value,
                'position': start,
                'replacement': replacement
            })
        
        return redacted_text, redactions
    
    def get_supported_pii_types(self) -> List[str]:
        """Return list of supported PII types"""
        return ['EMAIL', 'PHONE', 'SSN', 'DATE_OF_BIRTH', 'ADDRESS', 'ZIP_CODE', 'NAME']
