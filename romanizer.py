import re

'''
### Transcribing vowels ###
'''

vowel = {
    # 단모음 monophthongs
    'ㅏ' : 'a',
    'ㅓ' : 'eo',
    'ㅗ' : 'o',
    'ㅜ' : 'u',
    'ㅡ' : 'eu',
    'ㅣ' : 'i',
    'ㅐ' : 'ae',
    'ㅔ' : 'e',
    'ㅚ' : 'oe',
    'ㅟ' : 'wi',
    
    # 이중모음 diphthongs
    'ㅑ' : 'ya',
    'ㅕ' : 'yeo',
    'ㅛ' : 'yo',
    'ㅠ' : 'yu',
    'ㅒ' : 'yae',
    'ㅖ' : 'ye',
    'ㅘ' : 'wa',
    'ㅙ' : 'wae',
    'ㅝ' : 'wo',
    'ㅞ' : 'we',
    'ㅢ' : 'ui', # ‘ㅢ’는 ‘ㅣ’로 소리 나더라도 ‘ui’로 적는다.
}


# 초성 Choseong (Syllable Onset)
onset = {
    # 파열음 stops/plosives
    'ᄀ' : 'g',
    'ᄁ' : 'kk',
    'ᄏ' : 'k',
    'ᄃ' : 'd',
    'ᄄ' : 'tt',
    'ᄐ' : 't',
    'ᄇ' : 'b',
    'ᄈ' : 'pp',
    'ᄑ' : 'p',
    # 파찰음 affricates
    'ᄌ' : 'j',
    'ᄍ' : 'jj',
    'ᄎ' : 'ch',
    # 마찰음 fricatives
    'ᄉ' : 's',
    'ᄊ' : 'ss',
    'ᄒ' : 'h',
    # 비음 nasals
    'ᄂ' : 'n',
    'ᄆ' : 'm',
    # 유음 liquids
    'ᄅ' : 'r',
    # Null sound
    'ᄋ' : '',
}

# 종성 Jongsung (Syllable Coda) 
coda = {
    # 파열음 stops/plosives
    'ᆨ' : 'k',
    'ᆮ' : 't',
    'ᆸ' : 'p',
    # 'ᇁ' : 'p',
    # 비음 nasals
    'ᆫ' : 'n',
    'ᆼ' : 'ng',
    'ᆷ' : 'm',
    # 유음 liquids
    'ᆯ' : 'l',
    
    None: '',
}

double_consonant_final = {
    'ᆪ' : ('ᆨ', 'ᆺ'),
    'ᆬ' : ('ᆫ', 'ᆽ'),
    'ᆭ' : ('ᆫ', 'ᇂ'),
    'ᆰ' : ('ᆯ', 'ㄱ'),
    'ᆱ' : ('ᆯ', 'ᆷ'),
    'ᆲ' : ('ᆯ', 'ᆸ'),
    'ᆳ' : ('ᆯ', 'ᆺ'),
    'ᆴ' : ('ᆯ', 'ᇀ'),
    'ᆵ' : ('ᆯ', 'ᇁ'),
    'ᆶ' : ('ᆯ', 'ᇂ'),
    'ᆹ' : ('ᆸ', 'ᆺ'),
    'ᆻ' : ('ᆺ', 'ᆺ')
}

NULL_CONSONANT = 'ᄋ'

unicode_initial = [ 'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_initial = [ chr(initial_code) for initial_code in range(4352, 4371)]
unicode_medial = [ 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

#unicode_final = [ None,  'ㄱ',  'ㄲ',  'ㄳ',  'ㄴ',  'ㄵ',  'ㄶ',  'ㄷ',  'ㄹ',  'ㄺ',  'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ','ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',  'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_final = [ chr(final_code) for final_code in range(0x11a8, 0x11c3)]
unicode_final.insert(0, None)

unicode_compatible_consonants = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
unicode_compatible_finals =     ['ᆨ', 'ᆩ', 'ᆫ', 'ᆮ', '_', 'ᆯ', 'ᆷ', 'ᆸ', '_', 'ᆺ', 'ᆻ', 'ᆼ', 'ᆽ', '_', 'ᆾ', 'ᆿ', 'ᇀ', 'ᇁ', 'ᇂ']



class Syllable(object):
    def __init__(self, char):
        self.char = char
        _is_hangul, _separated = self.separate_syllable(char)
        if (_is_hangul):
            self.initial = unicode_initial[_separated[0]]
            self.medial = unicode_medial[_separated[1]]
            self.final = unicode_final[_separated[2]]
        else:
            self.initial = _separated[0]
            self.medial = None
            self.final = None
            
    def separate_syllable(self, char):
        if (self.is_hangul(char)):
            initial = (ord(char)-44032) // 588
            medial = ((ord(char)-44032) - 588 * initial) // 28
            final = (((ord(char)-44032) - 588 * initial) - 28 * medial)
            # print("Separate", initial,medial,final)
        else:
            initial = ord(char)
            medial = None
            final = None
            # print("NOT_HANGUL Separate", initial,medial,final)
            
        return self.is_hangul(char), [initial, medial, final]
    
    def construct_syllable(self, initial, medial, final):
        if self.is_hangul(self.char):
            initial = ord(initial) - 4352
            medial = unicode_medial.index(medial)
            if final is None:
                final = 0
            else:
                final = unicode_final.index(final)
            # print("Construct", initial,medial,final)
            constructed = chr((((initial * 588) + (medial * 28)) + final) + 44032)
        else:
            constructed = self.char
            
        self.char = constructed
        return constructed
    
    def is_hangul(self, char):
        return True if 0xAC00 <= ord(char) <= 0xD7A3 else False
    
    def final_to_initial(self, char):
        idx = unicode_compatible_finals.index(char)
        return unicode_initial[idx]
    
    def __repr__(self):
        self.construct_syllable(self.initial, self.medial, self.final)
        return self.char
    
    def __str__(self):
        self.char = self.construct_syllable(self.initial, self.medial, self.final)
        return self.char


class Pronouncer(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self.pronounced = ''.join([ str(c) for c in self.final_substitute()])
    
    def final_substitute(self):
        for idx, syllable in enumerate(self._syllables):
            try:
                next_syllable = self._syllables[idx+1]
            except IndexError:
                next_syllable = None
            
            try:    
                final_is_before_C = syllable.final and next_syllable.getattr(initial) not in (None, NULL_CONSONANT)
            except AttributeError:
                final_is_before_C = False

            try:    
                final_is_before_V = syllable.final and next_syllable.initial is None
            except AttributeError:
                final_is_before_V = False 
            
            # 1. 받침 ‘ㄲ, ㅋ’, ‘ㅅ, ㅆ, ㅈ, ㅊ, ㅌ’, ‘ㅍ’은 어말 또는 자음 앞에서 각각 대표음 [ㄱ, ㄷ, ㅂ]으로 발음한다.
            # 2. 겹받침 ‘ㄳ’, ‘ㄵ’, ‘ㄼ, ㄽ, ㄾ’, ‘ㅄ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㄴ, ㄹ, ㅂ]으로 발음한다.
            # 3. 겹받침 ‘ㄺ, ㄻ, ㄿ’은 어말 또는 자음 앞에서 각각 [ㄱ, ㅁ, ㅂ]으로 발음한다.
            # <-> 단, 국어의 로마자 표기법 규정에 의해 된소리되기는 표기에 반영하지 않으므로 제외.
#             if(syllable.final or final_is_before_C): 
#                 if(syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ᆰ']):
#                     syllable.final = 'ᆨ'
#                 elif(syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
#                     syllable.final = 'ᆮ'
#                 elif(syllable.final in ['ᇁ', 'ᆹ', 'ᆵ']):
#                     syllable.final = 'ᆸ'
#                 elif(syllable.final in ['ᆬ']):
#                     syllable.final = 'ᆫ'
#                 elif(syllable.final in ['ᆲ', 'ᆳ', 'ᆴ', 'ᆶ']):
#                     syllable.final = 'ᆯ'
#                 elif(syllable.final in ['ᆱ']):
#                     syllable.final = 'ᆷ'
            
            
            # 4. 받침 ‘ㅎ’의 발음은 다음과 같다.
            # if syllable.final in ['ᇂ', 'ᆭ', 'ᆶ']:
            #     if next_syllable:
            #         # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㄱ, ㄷ, ㅈ’이 결합되는 경우에는, 뒤 음절 첫소리와 합쳐서 [ㅋ, ㅌ, ㅊ]으로 발음한다.
            #         # ‘ㅎ(ㄶ, ㅀ)’ 뒤에 ‘ㅅ’이 결합되는 경우에는, ‘ㅅ’을 [ㅆ]으로 발음한다.
            #         if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ', 'ᄉ']:
            #             change_to = {'ᄀ': 'ᄏ','ᄃ': 'ᄐ','ᄌ':'ᄎ', 'ᄉ': 'ᄊ'}
            #             syllable.final = None
            #             next_syllable.initial = change_to[next_syllable.initial]
            #         # 3. ‘ㅎ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, [ㄴ]으로 발음한다.
            #         elif next_syllable.initial in ['ᄂ']:
            #             # TODO: [붙임] ‘ㄶ, ㅀ’ 뒤에 ‘ㄴ’이 결합되는 경우에는, ‘ㅎ’을 발음하지 않는다.
            #             if(syllable.final in ['ᆭ', 'ᆶ']):
            #                 if syllable.final == 'ᆭ':
            #                     syllable.final = 'ᆫ'
            #                 elif syllable.final == 'ᆶ':
            #                     syllable.final = 'ᆯ' 
            #             else:
            #                 syllable.final = 'ᆫ'
            #         #4. ‘ㅎ(ㄶ, ㅀ)’ 뒤에 모음으로 시작된 어미나 접미사가 결합되는 경우에는, 
            #         # ‘ㅎ’을 발음하지 않는다.
            #         elif next_syllable.initial == NULL_CONSONANT:
            #             if(syllable.final in ['ᆭ', 'ᆶ']):
            #                 if syllable.final == 'ᆭ':
            #                     syllable.final = 'ᆫ'
            #                 elif syllable.final == 'ᆶ':
            #                     syllable.final = 'ᆯ' 
            #             else:
            #                 syllable.final = None
            #         else:
            #             if (syllable.final == 'ᇂ'):
            #                 syllable.final = None
            #     else:
            #         if (syllable.final == 'ᇂ'):
            #             syllable.final = None
                        
                
#===================================================================================================================================
# 구개 음화 #========================================================================================================================       
#===================================================================================================================================
            # 종성 'ㄷ, ㅌ' 이 '이' 와 만나면 ㅈ, ㅊ 으로 변환
            # ex) 굳이 [구디 -> 구지] , 같이 [가티 -> 가치]
            if syllable.final in ['ᆮ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄋ'] and next_syllable.medial in ['ㅣ'] :
                        syllable.final = None
                        change_to = {'ᄋ': 'ᄌ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
            if syllable.final in ['ᇀ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄋ'] and next_syllable.medial in ['ㅣ'] :
                        syllable.final = None
                        change_to = {'ᄋ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
#===================================================================================================================================
# 유음화 #========================================================================================================================       
#===================================================================================================================================                        
            # 종성 'ㄴ' + 초성 'ㄹ' -> ㄹㄹ -> ex) 신라 [실라]
            # 종성 'ㄹ' + 초성 'ㄴ' -> ㄹㄹ -> ex) 칼날 [칼랄]
            if syllable.final in ['ᆫ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄅ']:
                        change_to = {'ᆫ': 'ᆯ'}
                        syllable.final = change_to[syllable.final]
                        
            if syllable.final in ['ᆯ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄂ']:                        
                        change_to = {'ᄂ': 'ᄅ'}
                        next_syllable.initial = change_to[next_syllable.initial]                  
                        
#===================================================================================================================================
# 격음화 #==========================================================================================================================       
#===================================================================================================================================                            
            
            if syllable.final in ['ᆨ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = None
                        change_to = {'ᄒ': 'ᄏ'}
                        next_syllable.initial = change_to[next_syllable.initial]

            if syllable.final in ['ᆰ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = 'ᆯ'
                        change_to = {'ᄒ': 'ᄏ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
            if syllable.final in ['ᆮ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = None
                        change_to = {'ᄒ': 'ᄐ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
            if syllable.final in ['ᆸ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = None
                        change_to = {'ᄒ': 'ᄑ'}
                        next_syllable.initial = change_to[next_syllable.initial]
            
            if syllable.final in ['ᆲ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = 'ᆯ'
                        change_to = {'ᄒ': 'ᄑ'}
                        next_syllable.initial = change_to[next_syllable.initial]  
                        
            if syllable.final in ['ᆽ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = None
                        change_to = {'ᄒ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]                                        

            if syllable.final in ['ᆬ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄒ']:
                        syllable.final = 'ᆫ'
                        change_to = {'ᄒ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]                  
            
            if syllable.final in ['ᇂ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄂ']:
                        syllable.final = 'ᆫ'
                        # change_to = {'ᄂ': 'ᄌ'}
                        # next_syllable.initial = change_to[next_syllable.initial]
                        
            if syllable.final in ['ᇂ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄉ']:
                        syllable.final = None
                        change_to = {'ᄉ': 'ㅆ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
            if syllable.final in ['ᇂ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ']:
                        syllable.final = None
                        change_to = {'ᄀ': 'ᄏ', 'ᄃ': 'ᄐ', 'ᄌ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]

            if syllable.final in ['ᆭ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ']:
                        syllable.final = 'ᆫ'
                        change_to = {'ᄀ': 'ᄏ', 'ᄃ': 'ᄐ', 'ᄌ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]                        

            if syllable.final in ['ᆶ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄀ', 'ᄃ', 'ᄌ']:
                        syllable.final = 'ᆯ'
                        change_to = {'ᄀ': 'ᄏ', 'ᄃ': 'ᄐ', 'ᄌ': 'ᄎ'}
                        next_syllable.initial = change_to[next_syllable.initial]
                        
                        
#===================================================================================================================================
# 자음 동화 #========================================================================================================================       
#===================================================================================================================================                            
            # 비음 ㅁ, ㅇ vs 탄음 ㄹ
            if syllable.final in ['ᆷ', 'ᆼ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄅ']:
                        change_to = {'ᄅ': 'ᄂ'}
                        next_syllable.initial = change_to[next_syllable.initial]

            # 불파음 ㄱ, ㄷ, ㅂ vs 비음 ㄴ, ㅁ            
            if syllable.final in ['ᆨ', 'ᆮ', 'ᆸ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄂ', 'ᄆ']:                        
                        change_to = {'ᆨ': 'ᆼ', 'ᆮ': 'ᆫ', 'ᆸ': 'ᆷ'}
                        syllable.final = change_to[syllable.final]                        
                        
            # 불파음 ㄱ, ㄷ, ㅂ vs 탄음 ㄹ           
            if syllable.final in ['ᆨ', 'ᆮ', 'ᆸ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄅ']:                        
                        change_to_initial = {'ᄅ': 'ᄂ'}
                        change_to_final = {'ᆨ': 'ᆼ', 'ᆮ': 'ᆫ', 'ᆸ': 'ᆷ'}
                        syllable.final = change_to_final[syllable.final]                                
                        next_syllable.initial = change_to_initial[next_syllable.initial]

#===================================================================================================================================
# 연음 #============================================================================================================================       
#===================================================================================================================================                           

            prolonged = {'ᆨ':'ᄀ', 'ᆩ':'ᄁ', 'ᆫ':'ᄂ', 'ᆮ':'ᄃ', 'ᆯ':'ᄅ', 'ᆷ':'ᄆ', 'ᆸ':'ᄇ', 'ᆺ':'ᄉ',
                  'ᆻ':'ᄊ', 'ᆽ':'ᄌ', 'ᆾ':'ᄎ', 'ᆿ':'ᄏ', 'ᇀ':'ᄐ', 'ᇁ':'ᄑ'}
    
            if syllable.final in ['ᆨ',  'ᆩ', 'ᆫ', 'ᆮ', 'ᆯ', 'ᆷ', 'ᆸ', 'ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᆿ',
                                  'ᇀ', 'ᇁ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄋ']:
                        change_to = {'ᄋ': prolonged.get(syllable.final)}
                        syllable.final = None
                        next_syllable.initial = change_to[next_syllable.initial]

            if syllable.final in ['ᇂ']:
                if next_syllable:
                    if next_syllable.initial in ['ᄋ']:
                        syllable.final = None
#                         change_to = {'ᄋ': 'ᄀ'}
#                         next_syllable.initial = change_to[next_syllable.initial]                                            
#===============================================================================================================================

            if(syllable.final or final_is_before_C): 
                if(syllable.final in ['ᆩ', 'ᆿ', 'ᆪ', 'ᆰ']):
                    syllable.final = 'ᆨ'
                elif(syllable.final in ['ᆺ', 'ᆻ', 'ᆽ', 'ᆾ', 'ᇀ']):
                    syllable.final = 'ᆮ'
                elif(syllable.final in ['ᇁ', 'ᆹ', 'ᆵ']):
                    syllable.final = 'ᆸ'
                elif(syllable.final in ['ᆬ']):
                    syllable.final = 'ᆫ'
                elif(syllable.final in ['ᆲ', 'ᆳ', 'ᆴ', 'ᆶ']):
                    syllable.final = 'ᆯ'
                elif(syllable.final in ['ᆱ']):
                    syllable.final = 'ᆷ'                        
                        
#===============================================================================================================================
            # 5. 홑받침이나 쌍받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는, 
            # 제 음가대로 뒤 음절 첫소리로 옮겨 발음한다. 
#             if next_syllable and final_is_before_C:
#                 if(next_syllable.initial == NULL_CONSONANT):
#                     next_syllable.initial = next_syllable.final_to_initial(syllable.final)
#                     syllable.final = None
                    
            # 6. 겹받침이 모음으로 시작된 조사나 어미, 접미사와 결합되는 경우에는, 
            # 뒤엣것만을 뒤 음절 첫소리로 옮겨 발음한다.(이 경우, ‘ㅅ’은 된소리로 발음함.)
#             if syllable.final in double_consonant_final:
#                 double_consonant = double_consonant_final[syllable.final]
#                 syllable.final = double_consonant[0]
#                 next_syllable.initial = next_syllable.final_to_initial(double_consonant[1])
        return self._syllables

    
class Romanizer(object):
    def __init__(self, text):
        self.text = text


    def romanize(self):
        pronounced = Pronouncer(self.text).pronounced
        print(pronounced)
        hangul = r"[가-힣ㄱ-ㅣ]"
        _romanized = []
        for char in pronounced:
            if (re.match(hangul, char)):
                s = Syllable(char)
                _romanized += onset[s.initial] + vowel[s.medial] + coda[s.final]
                
            else:
                _romanized += char
                
        return ''.join(_romanized).replace('lr', 'll')


if __name__ == "__main__":
    print(Romanizer("밝뭉너안미긁다잉").romanize())