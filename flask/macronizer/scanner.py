from macronizer import Macronizer


def scan_cltk_format(verse, meter):
    macronizer = Macronizer()
    SCANSIONS = {
        "-": [],
        "hexameter": [Macronizer.dactylichexameter],
        "elegiac": [Macronizer.dactylichexameter,
                    Macronizer.dactylicpentameter],
        "pentameter":  [Macronizer.dactylicpentameter],
        "hendecasyllable": [Macronizer.hendecasyllable],
        "iambic_trimeter_dimeter":
            [Macronizer.iambictrimeter, Macronizer.iambicdimeter]
    }
    macronizer.settext(verse)

    accented = macronizer.macronize(
        verse, performitoj=True, markambigs=True, tojson=False, minimaltext=True, ambiguousvowels=False)
    macronizer.scan(SCANSIONS[meter])

    def formatscansion(scanned_feet):
        def replacefeet(syllable):
            if(syllable == '-'):
                return '-'
            elif(syllable == 'S'):
                return '--'
            elif(syllable == 'D'):
                return '-UU'
            else:
                return ''

        scannedfeetarray = list(''.join(scanned_feet))
        replacedfeetarray = map(replacefeet, scannedfeetarray)
        print(replacedfeetarray)
        return ''.join(replacedfeetarray)

    scansion = formatscansion(macronizer.tokenization.scannedfeet)

    return {
        'original': verse,
        'scansion': scansion,
        "valid": len(scansion) > 0,
        'meter': meter,
        'syllable_count': len(scansion),
        'accented': accented,
        'scansion_notes': [],
        'syllables': [],
        'working_line': accented,
        'formatted': scansion
    }
