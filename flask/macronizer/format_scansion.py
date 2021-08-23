def formatScansion(scansion, verse, syllables):

    def isVowel(char):
        all_vowels = 'āēīōūȳĀĒĪŌŪȲaeiouyAEIOUY'
        return char in all_vowels

    scansion_array_formatted = []
    scansion_array = list(scansion)
    verse_subtr = verse
    if(len(scansion_array) == len(syllables)):
        # print ('\n\n\n')
        # print('### Analysis is valid!')
        # SYLLABLE LEVEL
        for syllable in syllables:
            #CHECKING FOR SPACES

            if(syllable in verse_subtr):
                # If syllable is first part of the verse ...
                # print(verse_subtr)
                # print(verse_subtr[:len(syllable)])
                # print(syllable)
                # print(verse_subtr[:len(syllable)] == syllable)
                if(verse_subtr[:len(syllable)] == syllable):
                    # ... subtract the syllable from the verse
                    verse_subtr = verse_subtr[len(syllable):]
                    versfuss = scansion_array.pop(0)
                    chars = list(syllable)

                    # CHAR LEVEL
                    for char in chars:
                        # print ('\n')
                        if(isVowel(char)):
                            #print(char + ' is Vowel')
                            scansion_array_formatted.append(versfuss)
                        else:
                            #print(char + ' is not a Vowel')
                            scansion_array_formatted.append(' ')

                # If first char of verse is a space ...
                elif(verse_subtr[0] == ' '):
                    # print('\n\n### Appending space.')
                    scansion_array_formatted.append(' ')
                    # print('### Removing space from the beginning of verse.')
                    verse_subtr = verse_subtr[1:]
                    verse_subtr = verse_subtr[len(syllable):]
                    versfuss = scansion_array.pop(0)
                    chars = list(syllable)

                    # CHAR LEVEL
                    for char in chars:
                        # print ('\n')
                        if(isVowel(char)):
                            #print(char + ' is Vowel')
                            scansion_array_formatted.append(versfuss)
                        else:
                            #print(char + ' is not a Vowel')
                            scansion_array_formatted.append(' ')
                else:
                    # print('### String broken or not equal to syllable strings!')
                    return False
            else:
                # print('### Syllable ' + syllable + ' not found in ' + verse_subtr)
                return False

    else:
        # print('### Length of syllables not equal to verse length!')
        return False


    scansion_formatted = ''.join(scansion_array_formatted)
    return scansion_formatted
