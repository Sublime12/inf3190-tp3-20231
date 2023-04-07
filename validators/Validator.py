import re

class ValidatorHandler:
    def __init__(self):
        self.data = []
    # name: Le nom du champ a valider
    # value: la valeur de l'element a valider
    # validators: les differentes validations a faire
    #   tableau des Validators
    # Retourne void
    def add(self, name, value, validators):
        self.data.append({
            'name': name,
            'value': value,
            'validators': validators,   
        })

    # Valide tous les valeurs passees
    # 
    def validate(self):
        errors = {}
        for el in self.data:
            name = el['name']
            value = el['value']
            validators = el['validators']
            error = {
                # 'name': name,
                'value': value,
                'messages': [],
            }

            for validator in validators:
                error_result = validator.handle(name, value)
                if not error_result['is_valid'] :
                    error['messages'].append(error_result['message'])
            
            if len(error['messages']) != 0:
                errors[name] = error
        
        return errors

    
class Required:
    def __init__(self) -> None:
        pass

    # Retourne {isValid, message:}
    # Verifie si la valeur passee est nulle
    def handle(self, name: str, value: str):
        if len(value) == 0:
            return {
                'is_valid': False,
                'message':  'L\'atribut ' + name + ' est requis'
            }
        
        return {
            'is_valid': True,
            'message': '',
        }

class ShouldNotContainsComma:
    def __init__(self) -> None:
        pass

    # Verifie si la chaine contient un comma
    def handle(self, name: str, value: str):
        if value.count(',') != 0:
            return {
                'is_valid': False,
                'message':  'L\'atribut ' + name + ' contient une virgule'
            }


        return {
            'is_valid': True,
            'message': '',
        }
    
class ShouldBeBetween:
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max

    def handle(self, name: str, value: str):
        if len(value) < self.min or len(value) > self.max:
            return {
                'is_valid': False,
                'message':  'La longueur de l\'atribut ' + name + ' n\'est pas entre ' + str(self.min) + ' et' + str(self.max)
            }
    
        return {
            'is_valid': True,
            'message': '',
        }

class NumberShouldBeBetween:
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max

    def handle(self, name: str, value: str):
        if value < self.min or value > self.max:
            return {
                'is_valid': False,
                'message':  'La longueur de l\'atribut ' + name + ' n\'est pas entre ' + str(self.min) + ' et' + str(self.max)
            }
    
        return {
            'is_valid': True,
            'message': '',
        }
    
class ShouldBeEmail:
    def __init__(self) -> None:
        # Regex for a ( :)kindy ) valid email format
        self._regex = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$'

    def handle(self, name: str, value: str):
        if (not re.match(self._regex, value)):
            
            return {
                'is_valid': False,
                'message':  'L\'atribut ' + name + ' n\'est pas une adresse mail valide'
            }
        
        return {
            'is_valid': True,
            'message': '',
        }
    
class AdressShouldBeValidCanadianFormat:
    def __init__(self) -> None:
        self._regex = '^$'