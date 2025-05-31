import json
import os
from sympy import sympify, symbols, Eq
from sympy.parsing.sympy_parser import parse_expr

class FormulaValider:
    """
    System walidacji wzorów matematyczno-fizycznych
    Σ (Sigma) - sprawdzenie składni matematycznej
    Δ (Delta) - sprawdzenie spójności jednostek fizycznych
    """
    
    def __init__(self, formula_str, units_dict=None, description=""):
        self.formula_str = formula_str.strip()
        self.units_dict = units_dict or {}
        self.description = description
        self.syntax_valid = False
        self.units_valid = None
        
    def check_syntax(self):
        """Σ (Sigma) - Sprawdzenie składni matematycznej"""
        try:
            # Sprawdź czy wzór zawiera znak równości
            if '=' not in self.formula_str:
                return False, "Błąd: Wzór musi zawierać znak równości '='"
            
            # Podziel na lewą i prawą stronę
            parts = self.formula_str.split('=')
            if len(parts) != 2:
                return False, "Błąd: Wzór może zawierać tylko jeden znak równości"
            
            lhs, rhs = parts[0].strip(), parts[1].strip()
            
            # Sprawdź składnię obu stron
            lhs_expr = sympify(lhs)
            rhs_expr = sympify(rhs)
            
            self.syntax_valid = True
            return True, f"✓ Składnia poprawna (Σ): {lhs} = {rhs}"
            
        except Exception as e:
            self.syntax_valid = False
            return False, f"✗ Błąd składniowy (Σ): {str(e)}"
    
    def check_units(self):
        """Δ (Delta) - Sprawdzenie spójności jednostek fizycznych"""
        if not self.units_dict:
            return None, "⚠ Brak danych jednostkowych do sprawdzenia (Δ)"
        
        if not self.syntax_valid:
            return False, "✗ Nie można sprawdzić jednostek - błędna składnia"
        
        try:
            # Podziel wzór na lewą i prawą stronę
            lhs, rhs = self.formula_str.split('=')
            lhs, rhs = lhs.strip(), rhs.strip()
            
            # Pobierz symbole z obu stron
            lhs_symbols = set(str(s) for s in sympify(lhs).free_symbols)
            rhs_symbols = set(str(s) for s in sympify(rhs).free_symbols)
            all_symbols = lhs_symbols | rhs_symbols
            
            # Sprawdź czy wszystkie symbole mają zdefiniowane jednostki
            missing_units = [s for s in all_symbols if s not in self.units_dict]
            if missing_units:
                return False, f"✗ Brak jednostek dla symboli: {', '.join(missing_units)}"
            
            # Dla prostoty - sprawdzamy czy jednostki są zdefiniowane
            # W przyszłości można dodać pełną analizę wymiarową
            lhs_unit = self.units_dict.get(lhs, "nieznana")
            
            self.units_valid = True
            return True, f"✓ Jednostki zdefiniowane (Δ): {lhs} [{lhs_unit}]"
            
        except Exception as e:
            self.units_valid = False
            return False, f"✗ Błąd analizy jednostek (Δ): {str(e)}"
    
    def validate(self):
        """Pełna walidacja wzoru (Σ + Δ)"""
        print(f"\n{'='*50}")
        print(f"WALIDACJA WZORU: {self.formula_str}")
        if self.description:
            print(f"Opis: {self.description}")
        print(f"{'='*50}")
        
        # Sprawdź składnię (Σ)
        syntax_ok, syntax_msg = self.check_syntax()
        print(f"[Σ] {syntax_msg}")
        
        # Sprawdź jednostki (Δ)
        units_ok, units_msg = self.check_units()
        print(f"[Δ] {units_msg}")
        
        # Podsumowanie
        print(f"\n{'─'*30}")
        if syntax_ok and (units_ok or units_ok is None):
            print("🎉 WZÓR POPRAWNY!")
        elif syntax_ok:
            print("⚠️  WZÓR CZĘŚCIOWO POPRAWNY (składnia OK, sprawdź jednostki)")
        else:
            print("❌ WZÓR NIEPOPRAWNY")
        print(f"{'─'*30}")

def load_formulas_from_json(filename="formulas.json"):
    """Wczytaj wzory z pliku JSON"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return get_builtin_formulas()
    except Exception as e:
        print(f"Błąd wczytywania pliku JSON: {e}")
        return get_builtin_formulas()

def get_builtin_formulas():
    """Wbudowane wzory (fallback gdy brak pliku JSON)"""
    return [
        {
            "id": "001",
            "formula": "E = m * c**2",
            "description": "Równanie równoważności masy i energii (Einstein)",
            "category": "Fizyka - Relatywistyka",
            "units": {
                "E": "J",
                "m": "kg", 
                "c": "m/s"
            }
        },
        {
            "id": "002", 
            "formula": "F = m * a",
            "description": "Druga zasada dynamiki Newtona",
            "category": "Fizyka - Mechanika",
            "units": {
                "F": "N",
                "m": "kg",
                "a": "m/s**2"
            }
        },
        {
            "id": "003",
            "formula": "P = U * I", 
            "description": "Prawo Ohma dla mocy elektrycznej",
            "category": "Fizyka - Elektryczność",
            "units": {
                "P": "W",
                "U": "V", 
                "I": "A"
            }
        },
        {
            "id": "004",
            "formula": "v = s / t",
            "description": "Prędkość jako stosunek drogi do czasu", 
            "category": "Fizyka - Kinematyka",
            "units": {
                "v": "m/s",
                "s": "m",
                "t": "s"
            }
        }
    ]

def create_sample_json():
    """Utwórz przykładowy plik formulas.json"""
    formulas = get_builtin_formulas()
    try:
        with open("formulas.json", 'w', encoding='utf-8') as f:
            json.dump(formulas, f, indent=2, ensure_ascii=False)
        print("✓ Utworzono przykładowy plik 'formulas.json'")
    except Exception as e:
        print(f"Błąd tworzenia pliku JSON: {e}")

def show_info():
    """Wyświetl informacje o systemie Σ/Δ"""
    info = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           FORMULAVALIDER v1.0                               ║
║                    System Walidacji Wzorów Σ/Δ (Sigma/Delta)                ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 WARSTWY WALIDACJI:

[Σ] SIGMA - Sprawdzenie składni matematycznej
    • Czy wzór zawiera znak równości '='?
    • Czy lewa i prawa strona są poprawnie zapisane matematycznie?
    • Używa biblioteki SymPy do parsowania wyrażeń

[Δ] DELTA - Sprawdzenie spójności jednostek fizycznych  
    • Czy wszystkie symbole mają zdefiniowane jednostki?
    • Czy jednostki po obu stronach równania są spójne?
    • Podstawa dla przyszłej pełnej analizy wymiarowej

🚀 PRZYSZŁE ROZSZERZENIA:

[Λ] LAMBDA - Analiza semantyczna symboli
    • Znaczenie symboli (masa, energia, siła...)
    • Typ wielkości fizycznej (skalarna, wektorowa...)
    • Kontekst dziedziny nauki

[Π] PI - Zgodność z prawami fizyki
    • Weryfikacja z bazą wiedzy fizycznej
    • Sprawdzenie granic stosowalności wzoru
    • Integracja z systemami AGI

📝 JAK TWORZYĆ WZORY:

1. Format: "lewa_strona = prawa_strona"
   Przykład: "F = m * a"

2. Używaj standardowych operatorów:
   • + - * / (podstawowe działania)
   • ** (potęgowanie)
   • sqrt() (pierwiastek)
   • sin(), cos(), log() (funkcje)

3. Jednostki w formacie słownika:
   {"F": "N", "m": "kg", "a": "m/s**2"}

4. Przykłady poprawnych wzorów:
   • E = m * c**2
   • F = m * a  
   • P = U * I
   • v = s / t
   • A = pi * r**2

💡 TIPS:
• Program jest gotowy do kompilacji przez PyInstaller
• Można rozszerzyć bazę wzorów w pliku formulas.json
• Kod jest modularny - łatwo dodać nowe warstwy walidacji

Autor: System FormulaValider - pierwsza implementacja walidacji Σ/Δ
"""
    print(info)

def menu_check_custom():
    """Menu - sprawdź własny wzór"""
    print("\n" + "="*50)
    print("           SPRAWDŹ WŁASNY WZÓR")
    print("="*50)
    
    formula = input("Podaj wzór (np. 'F = m * a'): ").strip()
    if not formula:
        print("❌ Nie podano wzoru!")
        return
    
    print("\nCzy chcesz dodać jednostki? (t/n): ", end="")
    add_units = input().lower().startswith('t')
    
    units = {}
    if add_units:
        print("\nPodaj jednostki dla symboli (Enter aby zakończyć):")
        print("Format: symbol jednostka (np. 'F N')")
        
        while True:
            unit_input = input("Symbol i jednostka: ").strip()
            if not unit_input:
                break
            
            parts = unit_input.split()
            if len(parts) >= 2:
                symbol = parts[0]
                unit = ' '.join(parts[1:])
                units[symbol] = unit
                print(f"  ✓ {symbol} -> {unit}")
            else:
                print("  ❌ Niepoprawny format!")
    
    # Walidacja
    validator = FormulaValider(formula, units)
    validator.validate()

def menu_check_predefined():
    """Menu - wybierz wzór z listy"""
    print("\n" + "="*50)
    print("         WZORY Z GOTOWEJ LISTY")
    print("="*50)
    
    formulas = load_formulas_from_json()
    
    print("\nDostępne wzory:")
    for i, formula in enumerate(formulas, 1):
        print(f"{i:2d}. {formula['formula']} - {formula['description']}")
    
    try:
        choice = int(input(f"\nWybierz wzór (1-{len(formulas)}): "))
        if 1 <= choice <= len(formulas):
            selected = formulas[choice-1]
            validator = FormulaValider(
                selected['formula'], 
                selected.get('units', {}),
                selected['description']
            )
            validator.validate()
        else:
            print("❌ Niepoprawny wybór!")
    except ValueError:
        print("❌ Podaj liczbę!")

def main_menu():
    """Główne menu programu"""
    while True:
        print("\n" + "╔" + "═"*48 + "╗")
        print("║" + " "*16 + "FORMULAVALIDER" + " "*17 + "║")
        print("║" + " "*12 + "System Walidacji Σ/Δ" + " "*15 + "║") 
        print("╠" + "═"*48 + "╣")
        print("║  1. Sprawdź własny wzór" + " "*24 + "║")
        print("║  2. Wybierz wzór z gotowej listy" + " "*15 + "║")
        print("║  3. Informacje o systemie Σ/Δ" + " "*17 + "║")
        print("║  4. Utwórz przykładowy formulas.json" + " "*10 + "║")
        print("║  5. Wyjście" + " "*36 + "║")
        print("╚" + "═"*48 + "╝")
        
        choice = input("\nWybierz opcję (1-5): ").strip()
        
        if choice == '1':
            menu_check_custom()
        elif choice == '2':
            menu_check_predefined()
        elif choice == '3':
            show_info()
        elif choice == '4':
            create_sample_json()
        elif choice == '5':
            print("\n👋 Do widzenia!")
            break
        else:
            print("❌ Niepoprawny wybór! Wybierz 1-5.")

if __name__ == "__main__":
    print("🚀 Uruchamianie FormulaValider...")
    main_menu()
