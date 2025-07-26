import re
import random
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
    
    def _generate_fake_email(self, original: str) -> str:
        """Generate a realistic fake email that maintains domain context"""
        fake_names = ['john.doe', 'jane.smith', 'alex.johnson', 'sarah.wilson', 'mike.brown']
        domains = ['example.com', 'sample.org', 'demo.net', 'test.com']
        
        # Try to preserve domain if it looks like a company domain
        original_parts = original.split('@')
        if len(original_parts) == 2:
            domain = original_parts[1].lower()
            if any(corp in domain for corp in ['gmail', 'yahoo', 'hotmail', 'outlook']):
                # Use generic domain for personal emails
                return f"{random.choice(fake_names)}@{random.choice(domains)}"
            else:
                # Keep similar structure for business emails
                return f"{random.choice(fake_names)}@example-company.com"
        
        return f"{random.choice(fake_names)}@{random.choice(domains)}"
    
    def _generate_fake_phone(self, original: str) -> str:
        """Generate a fake phone number maintaining format"""
        # Generate fake numbers in 555 range (reserved for fiction)
        area_code = random.choice(['555', '123', '456'])
        exchange = random.randint(100, 999)
        number = random.randint(1000, 9999)
        
        # Maintain original formatting
        if '(' in original and ')' in original:
            return f"({area_code}) {exchange}-{number}"
        elif '-' in original:
            return f"{area_code}-{exchange}-{number}"
        elif '.' in original:
            return f"{area_code}.{exchange}.{number}"
        else:
            return f"{area_code}{exchange}{number}"
    
    def _generate_fake_ssn(self, original: str) -> str:
        """Generate a fake SSN maintaining format"""
        # Use 999 prefix which is not issued
        fake_ssn = f"999{random.randint(10, 99)}{random.randint(1000, 9999)}"
        
        # Maintain original formatting
        if '-' in original:
            return f"{fake_ssn[:3]}-{fake_ssn[3:5]}-{fake_ssn[5:]}"
        else:
            return fake_ssn
    
    def _generate_fake_date(self, original: str) -> str:
        """Generate a fake date maintaining format"""
        fake_month = random.randint(1, 12)
        fake_day = random.randint(1, 28)  # Safe day for all months
        fake_year = random.randint(1960, 2000)
        
        # Maintain original format
        if '/' in original:
            if original.index('/') < 3:  # MM/DD/YYYY format
                return f"{fake_month:02d}/{fake_day:02d}/{fake_year}"
            else:  # YYYY/MM/DD format
                return f"{fake_year}/{fake_month:02d}/{fake_day:02d}"
        elif '-' in original:
            if original.index('-') < 3:  # MM-DD-YYYY format
                return f"{fake_month:02d}-{fake_day:02d}-{fake_year}"
            else:  # YYYY-MM-DD format
                return f"{fake_year}-{fake_month:02d}-{fake_day:02d}"
        
        return f"{fake_month}/{fake_day}/{fake_year}"
    
    def _generate_fake_address(self, original: str) -> str:
        """Generate a fake address maintaining street type"""
        fake_numbers = [123, 456, 789, 321, 654]
        fake_streets = ['Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'Main', 'First', 'Second']
        
        # Extract street type from original
        street_types = ['Street', 'St', 'Avenue', 'Ave', 'Road', 'Rd', 'Boulevard', 'Blvd', 
                       'Lane', 'Ln', 'Drive', 'Dr', 'Court', 'Ct', 'Place', 'Pl']
        
        street_type = 'Street'  # default
        for st_type in street_types:
            if st_type.lower() in original.lower():
                street_type = st_type
                break
        
        return f"{random.choice(fake_numbers)} {random.choice(fake_streets)} {street_type}"
    
    def _generate_fake_zip(self, original: str) -> str:
        """Generate a fake ZIP code maintaining format"""
        fake_zip = random.randint(10000, 99999)
        
        # Maintain format with +4 if present
        if '-' in original:
            fake_plus4 = random.randint(1000, 9999)
            return f"{fake_zip}-{fake_plus4}"
        else:
            return str(fake_zip)
    
    def _generate_fake_name(self, original: str) -> str:
        """Generate a fake name maintaining capitalization"""
        fake_first_names = ['John', 'Jane', 'Alex', 'Sarah', 'Mike', 'Lisa', 'David', 'Emma']
        fake_last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        
        # Check if it's likely a first name or last name based on common patterns
        if original.lower() in self.common_first_names:
            return random.choice(fake_first_names)
        elif original.lower() in self.common_last_names:
            return random.choice(fake_last_names)
        else:
            # Default to first name
            return random.choice(fake_first_names)
    
    def _get_replacement_generators(self):
        """Get replacement generators dictionary"""
        return {
            'email': self._generate_fake_email,
            'phone': self._generate_fake_phone,
            'ssn': self._generate_fake_ssn,
            'date_of_birth': self._generate_fake_date,
            'address': self._generate_fake_address,
            'zip_code': self._generate_fake_zip,
            'name': self._generate_fake_name
        }
    
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
        
        # Apply realistic replacements
        replacement_generators = self._get_replacement_generators()
        for pii_type, value, start, end in filtered_matches:
            # Generate appropriate replacement based on PII type
            if pii_type.lower() in replacement_generators:
                replacement = replacement_generators[pii_type.lower()](value)
            else:
                replacement = f"[SYNTHETIC_{pii_type}]"
            
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
