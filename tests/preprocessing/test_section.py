from training.preprocessing.datasets_.models import Section


def test_subsection_numbers_contain_no_newlines(law_matching_datasets):

    section = law_matching_datasets.acts["SARS-CoV-2-EindV"].sections[1]

    for subsection in section.subsections.values():
        assert "\n" not in subsection.subsection_number


def test_subsection_numbers_can_go_above_9():
    section = Section.from_dict(
        {
            "sectionNumber": "7",
            "sectionTitle": "Verbote",
            "valid_from": "02.11.2020",
            "valid_to": "15.12.2020",
            "text": "\n\n(1) Tanzlustbarkeiten und ähnliche Unternehmen im Sinne der Gewerbeordnung in der Fassung der Bekanntmachung vom 22. Februar 1999 (BGBl. I S. 202), die zuletzt durch Artikel 5 des Gesetzes vom 19. Juni 2020 (BGBl. I S. 1403) geändert worden ist, dürfen nicht für den Publikumsverkehr geöffnet werden.\n\n(2) Gaststätten mit der besonderen Betriebsart Diskotheken und ähnliche Betriebe im Sinne des Gaststättengesetzes in der Fassung der Bekanntmachung vom 20. November 1998 (BGBl. I S. 3418), das zuletzt durch Artikel 14 des Gesetzes vom 10. März 2017 (BGBl. I S. 420) geändert worden ist, dürfen nicht für den Publikumsverkehr geöffnet werden. Sie dürfen Speisen und Getränke zur Abholung oder zur Lieferung anbieten. Für die Abholung sind geeignete Vorkehrungen zur Steuerung der Kaufabwicklung und zur Vermeidung von Menschenansammlungen zu treffen. Auch in anderen Gaststätten sind Tanzveranstaltungen nicht zulässig.\n\n(3) Fitness- und Tanzstudios, Saunen, Dampfbäder, Thermen und ähnliche Einrichtungen sind geschlossen zu halten. Satz 1 gilt auch für entsprechende Bereiche in Hotels und ähnlichen Einrichtungen.\n\n(4) Gaststätten im Sinne des Gaststättengesetzes in der Fassung der Bekanntmachung vom 20. November 1998 (BGBl. I S. 3418), das zuletzt durch Artikel 14 des Gesetzes vom 10. März 2017 (BGBl. I S. 420) geändert worden ist, dürfen nicht für den Publikumsverkehr geöffnet werden. Sie dürfen Speisen und Getränke zur Abholung oder zur Lieferung anbieten. Für die Abholung sind geeignete Vorkehrungen zur Steuerung der Kaufabwicklung und zur Vermeidung von Menschenansammlungen zu treffen. Satz 1 gilt nicht für den Betrieb von Kantinen.\n\n(5) Weihnachtsmärkte und Jahrmärkte sind verboten.\n\n(5a) Bei der Öffnung von Verkaufsstellen, Kaufhäusern und Einkaufszentren (Malls) gilt für die Steuerung des Zutritts und zur Sicherung des Mindestabstandes ein Richtwert von maximal einer Person (Kundinnen und Kunden) pro 10 Quadratmeter Verkaufsfläche und Geschäftsraum. Unterschreiten die Verkaufsfläche oder der Geschäftsraum eine Größe von 10 Quadratmeter, so darf jeweils maximal eine Kundin oder ein Kunde eingelassen werden. Aufenthaltsanreize dürfen nicht geschaffen werden. § 1 Absatz 4 gilt entsprechend.\n\n(6) Der Ausschank, die Abgabe und der Verkauf von alkoholischen Getränken sind in der Zeit von 23 Uhr bis 6 Uhr des Folgetages verboten.\n\n(7) Dienstleistungsgewerbe im Bereich der Körperpflege wie Kosmetikstudios, Massagepraxen, Tattoo-Studios und ähnliche Betriebe dürfen weder für den Publikumsverkehr geöffnet werden noch ihre Dienste anbieten. Satz 1 gilt nicht für Friseurbetriebe und medizinisch notwendige Behandlungen, insbesondere Physio-, Ergo- und Logotherapie, Podologie, Fußpflege und Heilpraktiker.\n\n(8) Kinos, Theater, Opern, Konzerthäuser, Museen, Gedenkstätten und kulturelle Veranstaltungsstätten in öffentlicher und privater Trägerschaft dürfen nicht für den Publikumsverkehr geöffnet werden. Der Leihbetrieb von Bibliotheken ist zulässig.\n\n(9) Vergnügungsstätten im Sinne der Baunutzungsverordnung in der Fassung der Bekanntmachung vom 21. November 2017 (BGBl. I S. 3786), Freizeitparks, Betriebe für Freizeitaktivitäten sowie Spielhallen, Spielbanken, Wettvermittlungsstellen und ähnliche Betriebe dürfen nicht für den Publikumsverkehr geöffnet werden.\n\n(10) Die Tierhäuser und das Aquarium des Zoologischen Gartens Berlin und die Tierhäuser des Tierparks Berlin-Friedrichsfelde dürfen nicht für den Publikumsverkehr geöffnet werden.\n\n(11) Touristische Übernachtungen in Hotels und anderen Beherbergungsbetrieben sind untersagt.\n\n(12) Prostitutionsgewerbe im Sinne des Prostituiertenschutzgesetzes vom 21. Oktober 2016 (BGBl. I S. 2372), das durch Artikel 57 des Gesetzes vom 20. November 2019 (BGBl. I S. 1626) geändert worden ist, dürfen weder für den Publikumsverkehr geöffnet werden, noch ihre Dienste außerhalb ihrer Betriebsstätte erbringen. Die Erbringung und Inanspruchnahme sexueller Dienstleistungen mit Körperkontakt und erotische Massagen sind untersagt.",
        },
        "SARS-CoV-2-Infektionsschutzverordnung",
    )
    assert section.subsections.keys() == 12


first = {
    "sectionNumber": "5",
    "sectionTitle": "Weitere Hygiene- und Schutzregeln für besondere Bereiche",
    "valid_from": "02.11.2020",
    "valid_to": "15.12.2020",
    "text": "\n\n(1) In geschlossenen Räumen darf gemeinsam nur professionell oder im Rahmen der Religionsausübung "
    "gesungen werden, wenn die im Hygienerahmenkonzept der für Kultur zuständigen Senatsverwaltung nach § 2 "
    "Absatz 3 festgelegten Hygiene- und Infektionsschutzstandards eingehalten werden. Satz 1 gilt nicht für "
    "in § 1 Absatz 3 genannte Personen.\n\n(2) Bei Versammlungen im Sinne von Artikel 8 des Grundgesetzes und "
    "Artikel 26 der Verfassung von Berlin hat die die Versammlung veranstaltende Person ein individuelles "
    "Schutz- und Hygienekonzept zu erstellen, aus dem die vorgesehenen Maßnahmen zur Gewährleistung des "
    "Mindestabstands und der jeweils zu beachtenden Hygieneregeln, wie erforderlichenfalls das Tragen einer "
    "Mund-Nasen-Bedeckung oder der Verzicht auf gemeinsame Sprechchöre durch die Teilnehmenden während der "
    "Versammlung, sowie zur Gewährleistung der nach der nutzbaren Fläche des Versammlungsortes zulässigen "
    "Teilnehmendenzahl bei der Durchführung der Versammlung hervorgehen. Die Versammlungsbehörde kann die "
    "Vorlage dieses Schutz- und Hygienekonzepts von der die Versammlung veranstaltenden Person verlangen und "
    "beim zuständigen Gesundheitsamt eine infektionsschutzrechtliche Bewertung des Konzepts einholen. Bei der "
    "Durchführung der Versammlungen ist die Einhaltung des Schutz- und Hygienekonzepts von der "
    "Versammlungsleitung sicherzustellen.\n\n(3) Zugelassene Krankenhäuser dürfen planbare Aufnahmen, "
    "Operationen und Eingriffe unter der Voraussetzung durchführen, dass Reservierungs- und Freihaltevorgaben "
    "eingehalten werden und die Rückkehr in einen Krisenmodus wegen einer Verschärfung der Pandemielage "
    "jederzeit kurzfristig umgesetzt werden kann. Das Nähere hierzu und zu Besuchsregelungen bestimmt die für "
    "Gesundheit zuständige Senatsverwaltung durch Rechtsverordnung nach Maßgabe des § 32 Satz 1 des "
    "Infektionsschutzgesetzes.\n\n(3a) Im Bereich der Eingliederungshilfe und der Sozialhilfe kann die für "
    "Soziales zuständige Senatsverwaltung Regelungen durch Rechtsverordnung nach Maßgabe des § 32 Satz 1 des "
    "Infektionsschutzgesetzes bestimmen, die eine Grundversorgung der Leistungsberechtigten sicherstellen. "
    "Leistungserbringer mit Vereinbarungen nach § 123 Neuntes Buch Sozialgesetzbuch oder § 75 Zwölftes Buch "
    "Sozialgesetzbuch - Sozialhilfe - (Artikel 1 des Gesetzes vom 27. Dezember 2003, BGBl. I S. 3022, 3023), "
    "das zuletzt durch Artikel 11 des Gesetzes vom 14. Dezember 2019 (BGBl. I S. 2789) geändert worden ist, "
    "sind zur Abwendung von Gefahren für Mitarbeitende und Leistungsberechtigte befugt, das Personal "
    "abweichend von den Leistungsvereinbarungen, aber im inhaltlichen Rahmen des Leistungsbereichs, "
    "einzusetzen. Die Grundversorgung der Leistungsberechtigten ist sicherzustellen.\n\n(4) Der Zutritt zu "
    "Kaufhäusern und Einkaufszentren (Malls) ist vom Betreiber gesondert zu regulieren. Aufenthaltsanreize in "
    "Kaufhäusern und Einkaufszentren (Malls) dürfen nicht geschaffen werden.\n\n(5) Auf nach dieser "
    "Verordnung zulässigen Veranstaltungen sind die Bestuhlung und Anordnung der Tische so vorzunehmen, "
    "dass zwischen Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, ein Mindestabstand von 1,"
    "5 Metern eingehalten wird oder ein ausreichender Infektionsschutz durch andere Schutzmaßnahmen oder "
    "Schutzvorrichtungen zur Verringerung der Ausbreitung übertragungsfähiger Tröpfchenpartikel gewährleistet "
    "werden kann. Abweichend von Satz 1 sowie § 1 Absatz 2 Satz 1 dürfen Gruppen von bis zu zwei Personen mit "
    "weniger als 1,5 Metern Abstand untereinander platziert werden. Bei Veranstaltungen im Freien kann der "
    "Mindestabstand nach Satz 1 unterschritten werden, sofern der Schutz vor Tröpfcheninfektionen und "
    "Aerosolen sichergestellt ist.\n\n(6) In Kantinen dürfen Speisen und Getränke nur an Tischen sowie "
    "sitzend an Theken und Tresen verzehrt werden. Die Bestuhlung und Anordnung der Tische ist so "
    "vorzunehmen, dass zwischen Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, "
    "ein Mindestabstand von 1,5 Metern eingehalten wird. Abweichend von Satz 2 sowie § 1 Absatz 2 Satz 1 "
    "dürfen Gruppen von bis zu zwei Personen mit weniger als 1,5 Metern Abstand untereinander an einem Tisch "
    "sitzen. Im Freien kann der Mindestabstand nach Satz 2 unterschritten werden, sofern der Schutz vor "
    "Tröpfcheninfektionen und Aerosolen sichergestellt ist. Im Abstandsbereich dürfen sich keine Personen "
    "aufhalten. Ein verstärktes Reinigungs- und Desinfektionsregime ist sicherzustellen.\n\n(7) Sport darf "
    "vorbehaltlich des Satzes 2 nur alleine oder mit einer anderen Person kontaktfrei und unter Einhaltung "
    "der Abstandsregelungen nach § 1 Absatz 2 erfolgen. Für folgende Personengruppen gilt die Beschränkung "
    "des Satz 1 nicht:\na) für den Personenkreis gemäß § 1 Absatz 3,\nb) für Bundes- und "
    "Landeskaderathletinnen und -athleten, Profiligen und Berufssportlerinnen und Berufssportler und\nc) für "
    "Kinder im Alter von bis zu 12 Jahren, wenn der Sport im Freien in festen Gruppen von maximal 10 "
    "anwesenden Personen zuzüglich einer betreuenden Person ausgeübt wird.\n\nDie Verantwortlichen sind "
    "verpflichtet vor Beginn der Sporteinheit auf die Einhaltung des Schutz- und Hygienekonzepts nach § 2 "
    "Absatz 1 hinzuweisen und für dessen Umsetzung Sorge zu tragen. Regelungen über den Sport an öffentlichen "
    "Schulen und Schulen in freier Trägerschaft, an Einrichtungen der Berufsbildung sowie als "
    "studienbezogener Lehrbetrieb der Hochschulen gehen diesem Absatz und Absatz 7a vor.\n\n(7a)  Gedeckte "
    "Sportanlagen (Sporthallen) dürfen nur geöffnet werden, soweit dies erforderlich ist\na) für den Sport "
    "des in § 5 Absatz 7 Satz 2 Buchstabe b genannten Personenkreises,\nb) für den Pferdesport in dem unter "
    "Tierschutzgesichtspunkten zwingend erforderlichen Umfang.\n\nAnsonsten bleiben sie geschlossen.\n\n(8) "
    "Der professionelle sportliche Wettkampfbetrieb in der Bundesliga und den internationalen Ligen sowie "
    "vergleichbaren professionellen Wettkampfsystemen ist zulässig, soweit er im Rahmen eines Nutzungs- und "
    "Hygienekonzeptes des jeweiligen Sportfachverbandes stattfindet. Zuschauende sind untersagt. Satz 2 gilt "
    "nicht für die für den Spielbetrieb erforderlichen Personen.\n\n(9) Schwimmbäder dürfen ausschließlich "
    "für die Nutzung durch Bundes- und Landeskaderathletinnen und -athleten, Profiligen und "
    "Berufssportlerinnen und -sportler, für den Sport als Unterrichtsfach an öffentlichen Schulen und Schulen "
    "in freier Trägerschaft, an Einrichtungen der Berufsbildung und als studienbezogener Lehrbetrieb der "
    "Hochschulen sowie für therapeutische Behandlungen geöffnet werden. Frei- und Strandbäder bleiben "
    "geschlossen.\n\n(10) Im Bereich der Kindertagesförderung kann die für Jugend und Familie zuständige "
    "Senatsverwaltung in Fällen eines auf Grund der Infektionslage eingeschränkten Einsatzes von Fachpersonal "
    "in den Einrichtungen Näheres bestimmen, um dennoch die Betreuungsumfänge unter Beachtung der "
    "Hygienevorgaben nach dem Kindertagesförderungsgesetz vom 23. Juni 2005 (GVBl. S. 322), das zuletzt durch "
    "Artikel 1 des Gesetzes vom 11. Juni 2020 (GVBl. S. 535) geändert worden ist, erfüllen zu können.\n\n(11) "
    "(aufgehoben)\n\n(12) Staatliche, private und konfessionelle Hochschulen einschließlich ihrer "
    "Einrichtungen dürfen bis zum 31. März 2021 nicht für den Publikumsverkehr geöffnet werden. Die "
    "Hochschulen führen ihren Lehrbetrieb im Wintersemester 2020/2021 ab 2. November 2020 grundsätzlich mit "
    "Online-Formaten und nicht im Präsenzlehrbetrieb durch. Praxisformate, die nicht digital durchführbar "
    "sind, und Prüfungen dürfen unter Beachtung der grundsätzlichen Pflichten, der Schutz- und Hygieneregeln "
    "nach Teil 1 sowie der jeweils in den Hochschulen geltenden besonderen Bestimmungen in Präsenzform "
    "durchgeführt werden. Zulässig nach Satz 3 sind insbesondere\n1. Praxisformate, die spezielle Labor- und "
    "Arbeitsräume an den Hochschulen erfordern,\n2. praktischer Unterricht in medizinisch-klinischen "
    "Studiengängen,\n3. künstlerischer Unterricht,\n4. sportpraktische Übungen und\n5. Präsenzformate zur "
    "Einführung von Studienanfängerinnen und Studienanfängern.\n\nIn Praxisformaten nach Satz 4 soll die "
    "maximale Anzahl von 25 teilnehmenden Studierenden grundsätzlich nicht überschritten werden. In "
    "begründeten Fällen können die Hochschulen Personen abweichend von Satz 1 begrenzten Zutritt gestatten. "
    "Satz 1 gilt nicht für wissenschaftliche Bibliotheken und den Botanischen Garten.",
}
second = {
    "sectionNumber": "5",
    "sectionTitle": "Weitere Hygiene- und Schutzregeln für besondere Bereiche",
    "valid_from": "02.11.2020",
    "valid_to": "15.12.2020",
    "text": "\n\n(1) In geschlossenen Räumen darf gemeinsam nur professionell oder im Rahmen der Religionsausübung "
    "gesungen werden, wenn die nach § 2 Absatz 3 in einem Hygienerahmenkonzept oder in einer Rechtsverordnung "
    "der für Kultur zuständigen Senatsverwaltung festgelegten Hygiene- und Infektionsschutzstandards "
    "eingehalten werden. Satz 1 gilt nicht für in § 1 Absatz 3 genannte Personen.\n\n(2) Bei Versammlungen im "
    "Sinne von Artikel 8 des Grundgesetzes und Artikel 26 der Verfassung von Berlin hat die die Versammlung "
    "veranstaltende Person ein individuelles Schutz- und Hygienekonzept zu erstellen, aus dem die "
    "vorgesehenen Maßnahmen zur Gewährleistung des Mindestabstands und der jeweils zu beachtenden "
    "Hygieneregeln, wie erforderlichenfalls das Tragen einer Mund-Nasen-Bedeckung oder der Verzicht auf "
    "gemeinsame Sprechchöre durch die Teilnehmenden während der Versammlung, sowie zur Gewährleistung der "
    "nach der nutzbaren Fläche des Versammlungsortes zulässigen Teilnehmendenzahl bei der Durchführung der "
    "Versammlung hervorgehen. Die Versammlungsbehörde kann die Vorlage dieses Schutz- und Hygienekonzepts von "
    "der die Versammlung veranstaltenden Person verlangen und beim zuständigen Gesundheitsamt eine "
    "infektionsschutzrechtliche Bewertung des Konzepts einholen. Bei der Durchführung der Versammlungen ist "
    "die Einhaltung des Schutz- und Hygienekonzepts von der Versammlungsleitung sicherzustellen.\n\n(3) "
    "Zugelassene Krankenhäuser dürfen planbare Aufnahmen, Operationen und Eingriffe unter der Voraussetzung "
    "durchführen, dass Reservierungs- und Freihaltevorgaben eingehalten werden und die Rückkehr in einen "
    "Krisenmodus wegen einer Verschärfung der Pandemielage jederzeit kurzfristig umgesetzt werden kann. Das "
    "Nähere hierzu und zu Besuchsregelungen bestimmt die für Gesundheit zuständige Senatsverwaltung durch "
    "Rechtsverordnung nach Maßgabe des § 32 Satz 1 des Infektionsschutzgesetzes.\n\n(3a) Im Bereich der "
    "Eingliederungshilfe und der Sozialhilfe kann die für Soziales zuständige Senatsverwaltung Regelungen "
    "durch Rechtsverordnung nach Maßgabe des § 32 Satz 1 des Infektionsschutzgesetzes bestimmen, "
    "die eine Grundversorgung der Leistungsberechtigten sicherstellen. Leistungserbringer mit Vereinbarungen "
    "nach § 123 Neuntes Buch Sozialgesetzbuch oder § 75 Zwölftes Buch Sozialgesetzbuch - Sozialhilfe - ("
    "Artikel 1 des Gesetzes vom 27. Dezember 2003, BGBl. I S. 3022, 3023), das zuletzt durch Artikel 11 des "
    "Gesetzes vom 14. Dezember 2019 (BGBl. I S. 2789) geändert worden ist, sind zur Abwendung von Gefahren "
    "für Mitarbeitende und Leistungsberechtigte befugt, das Personal abweichend von den "
    "Leistungsvereinbarungen, aber im inhaltlichen Rahmen des Leistungsbereichs, einzusetzen. Die "
    "Grundversorgung der Leistungsberechtigten ist sicherzustellen.\n\n(4) Bei der Öffnung von "
    "Verkaufsstellen, Kaufhäusern und Einkaufszentren (Malls) gilt für die Steuerung des Zutritts und zur "
    "Sicherung des Mindestabstandes ein Richtwert für die maximal zulässige Anzahl von Kundinnen und Kunden "
    "je Verkaufsfläche oder Geschäftsraum. Bei Geschäften mit einer Verkaufsfläche von bis zu 800 "
    "Quadratmetern gilt ein Richtwert von insgesamt höchstens einer Kundin oder einem Kunden pro 10 "
    "Quadratmetern Verkaufsfläche. Bei Geschäften mit einer Verkaufsfläche ab 801 Quadratmetern insgesamt "
    "gilt auf einer Fläche von 800 Quadratmetern ein Richtwert von höchstens einer Kundin oder einem Kunden "
    "pro 10 Quadratmetern Verkaufsfläche und auf der 800 Quadratmeter übersteigenden Fläche von höchstens "
    "einer Kundin oder einem Kunden pro 20 Quadratmeter Verkaufsfläche. Für Einkaufszentren ist die jeweilige "
    "Gesamtverkaufsfläche maßgeblich. Unterschreiten die Verkaufsfläche oder der Geschäftsraum eine Größe von "
    "20 Quadratmetern, darf jeweils höchstens eine Kundin oder ein Kunde eingelassen werden. "
    "Aufenthaltsanreize dürfen nicht geschaffen werden. Insbesondere sind die Verkehrsflächen von "
    "Verkaufsständen freizuhalten. § 1 Absatz 4 gilt entsprechend.\n\n(5) Auf nach dieser Verordnung "
    "zulässigen Veranstaltungen sind die Bestuhlung und Anordnung der Tische so vorzunehmen, dass zwischen "
    "Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, ein Mindestabstand von 1,"
    "5 Metern eingehalten wird oder ein ausreichender Infektionsschutz durch andere Schutzmaßnahmen oder "
    "Schutzvorrichtungen zur Verringerung der Ausbreitung übertragungsfähiger Tröpfchenpartikel gewährleistet "
    "werden kann. Abweichend von Satz 1 sowie § 1 Absatz 2 Satz 1 dürfen Gruppen von bis zu zwei Personen mit "
    "weniger als 1,5 Metern Abstand untereinander platziert werden. Bei Veranstaltungen im Freien kann der "
    "Mindestabstand nach Satz 1 unterschritten werden, sofern der Schutz vor Tröpfcheninfektionen und "
    "Aerosolen sichergestellt ist.\n\n(6) In Kantinen dürfen Speisen und Getränke nur an Tischen sowie "
    "sitzend an Theken und Tresen verzehrt werden. Die Bestuhlung und Anordnung der Tische ist so "
    "vorzunehmen, dass zwischen Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, "
    "ein Mindestabstand von 1,5 Metern eingehalten wird. Abweichend von Satz 2 sowie § 1 Absatz 2 Satz 1 "
    "dürfen Gruppen von bis zu zwei Personen mit weniger als 1,5 Metern Abstand untereinander an einem Tisch "
    "sitzen. Im Freien kann der Mindestabstand nach Satz 2 unterschritten werden, sofern der Schutz vor "
    "Tröpfcheninfektionen und Aerosolen sichergestellt ist. Im Abstandsbereich dürfen sich keine Personen "
    "aufhalten. Ein verstärktes Reinigungs- und Desinfektionsregime ist sicherzustellen.\n\n(7) Sport darf "
    "vorbehaltlich des Satzes 2 nur alleine oder mit einer anderen Person kontaktfrei und unter Einhaltung "
    "der Abstandsregelungen nach § 1 Absatz 2 erfolgen. Für folgende Personengruppen gilt die Beschränkung "
    "des Satz 1 nicht:\na) für den Personenkreis gemäß § 1 Absatz 3,\nb) für Bundes- und "
    "Landeskaderathletinnen und -athleten, Profiligen und Berufssportlerinnen und Berufssportler,"
    "\nc) für Kinder im Alter von bis zu 12 Jahren, wenn der Sport im Freien in festen Gruppen von maximal 10 "
    "anwesenden Personen zuzüglich einer betreuenden Person ausgeübt wird und\nd) für ärztlich verordneten "
    "Rehabilitationssport oder ärztlich verordnetes Funktionstraining im Sinne des § 64 Absatz 1 Nummer 3 und "
    "4 des Neunten Buches Sozialgesetzbuch vom 23. Dezember 2016 (BGBl. I S. 3234), das zuletzt durch "
    "Artikel 3 Absatz 6 des Gesetzes vom 9. Oktober 2020 (BGBl. I S. 2075) geändert worden ist, "
    "in festen Gruppen von bis zu höchstens zehn Personen zuzüglich einer übungsleitenden Person; bei "
    "besonderen im Einzelfall zu begründenden Härtefällen ist die Beteiligung weiterer Personen zulässig, "
    "soweit dies zwingend notwendig ist, um den Teilnehmenden die Ausübung des Rehabilitationssports oder "
    "Funktionstrainings zu ermöglichen.\n\nDie Verantwortlichen sind verpflichtet vor Beginn der Sporteinheit "
    "auf die Einhaltung des Schutz- und Hygienekonzepts nach § 2 Absatz 1 hinzuweisen und für dessen "
    "Umsetzung Sorge zu tragen. Regelungen über den Sport an öffentlichen Schulen und Schulen in freier "
    "Trägerschaft, an Einrichtungen der Berufsbildung sowie als studienbezogener Lehrbetrieb der Hochschulen "
    "gehen diesem Absatz und Absatz 7a vor.\n\n(7a) Gedeckte Sportanlagen dürfen nur geöffnet werden, "
    "soweit dies erforderlich ist\na) für den Sport des in § 5 Absatz 7 Satz 2 Buchstabe b genannten "
    "Personenkreises,\nb) für den Pferdesport in dem unter Tierschutzgesichtspunkten zwingend erforderlichen "
    "Umfang,\nc) für therapeutische Behandlungen sowie Nutzungen nach Maßgabe des Absatz 7 Satz 2 Buchstabe "
    "d.\n\nAnsonsten bleiben sie geschlossen.\n\n(8) Der professionelle sportliche Wettkampfbetrieb in der "
    "Bundesliga und den internationalen Ligen sowie vergleichbaren professionellen Wettkampfsystemen ist "
    "zulässig, soweit er im Rahmen eines Nutzungs- und Hygienekonzeptes des jeweiligen Sportfachverbandes "
    "stattfindet. Zuschauende sind untersagt. Satz 2 gilt nicht für die für den Spielbetrieb erforderlichen "
    "Personen.\n\n(9) Schwimmbäder dürfen ausschließlich für die Nutzung durch Bundes- und "
    "Landeskaderathletinnen und -athleten, Profiligen und Berufssportlerinnen und -sportler, für den Sport "
    "als Unterrichtsfach an öffentlichen Schulen und Schulen in freier Trägerschaft, an Einrichtungen der "
    "Berufsbildung und als studienbezogener Lehrbetrieb der Hochschulen, für therapeutische Behandlung sowie "
    "Nutzungen nach Maßgabe des Absatz 7 Satz 2 Buchstabe d geöffnet werden. Frei- und Strandbäder bleiben "
    "geschlossen.\n\n(10) Im Bereich der Kindertagesförderung kann die für Jugend und Familie zuständige "
    "Senatsverwaltung in Fällen eines auf Grund der Infektionslage eingeschränkten Einsatzes von Fachpersonal "
    "in den Einrichtungen Näheres bestimmen, um dennoch die Betreuungsumfänge unter Beachtung der "
    "Hygienevorgaben nach dem Kindertagesförderungsgesetz vom 23. Juni 2005 (GVBl. S. 322), das zuletzt durch "
    "Artikel 1 des Gesetzes vom 11. Juni 2020 (GVBl. S. 535) geändert worden ist, erfüllen zu können.\n\n(11) "
    "(aufgehoben)\n\n(12) Staatliche, private und konfessionelle Hochschulen einschließlich ihrer "
    "Einrichtungen dürfen bis zum 31. März 2021 nicht für den Publikumsverkehr geöffnet werden. Die "
    "Hochschulen führen ihren Lehrbetrieb im Wintersemester 2020/2021 ab 2. November 2020 grundsätzlich mit "
    "Online-Formaten und nicht im Präsenzlehrbetrieb durch. Praxisformate, die nicht digital durchführbar "
    "sind, und Prüfungen dürfen unter Beachtung der grundsätzlichen Pflichten, der Schutz- und Hygieneregeln "
    "nach Teil 1 sowie der jeweils in den Hochschulen geltenden besonderen Bestimmungen in Präsenzform "
    "durchgeführt werden. Zulässig nach Satz 3 sind insbesondere\n1. Praxisformate, die spezielle Labor- und "
    "Arbeitsräume an den Hochschulen erfordern,\n2. praktischer Unterricht in medizinisch-klinischen "
    "Studiengängen,\n3. künstlerischer Unterricht,\n4. sportpraktische Übungen und\n5. Präsenzformate zur "
    "Einführung von Studienanfängerinnen und Studienanfängern.\n\nIn Praxisformaten nach Satz 4 soll die "
    "maximale Anzahl von 25 teilnehmenden Studierenden grundsätzlich nicht überschritten werden. In "
    "begründeten Fällen können die Hochschulen Personen abweichend von Satz 1 begrenzten Zutritt gestatten. "
    "Satz 1 gilt nicht für wissenschaftliche Bibliotheken und den Botanischen Garten.",
}

third = {
    "sectionNumber": "5",
    "sectionTitle": "Weitere Hygiene- und Schutzregeln für besondere Bereiche",
    "valid_from": "02.11.2020",
    "valid_to": "15.12.2020",
    "text": "\n\n(1) In geschlossenen Räumen darf gemeinsam nur professionell oder im Rahmen der Religionsausübung gesungen werden, wenn die nach § 2 Absatz 3 in einem Hygienerahmenkonzept oder in einer Rechtsverordnung der für Kultur zuständigen Senatsverwaltung festgelegten Hygiene- und Infektionsschutzstandards eingehalten werden. Satz 1 gilt nicht für in § 1 Absatz 3 genannte Personen.\n\n(2) Bei Versammlungen im Sinne von Artikel 8 des Grundgesetzes und Artikel 26 der Verfassung von Berlin hat die die Versammlung veranstaltende Person ein individuelles Schutz- und Hygienekonzept zu erstellen, aus dem die vorgesehenen Maßnahmen zur Gewährleistung des Mindestabstands und der jeweils zu beachtenden Hygieneregeln, wie erforderlichenfalls das Tragen einer Mund-Nasen-Bedeckung oder der Verzicht auf gemeinsame Sprechchöre durch die Teilnehmenden während der Versammlung, sowie zur Gewährleistung der nach der nutzbaren Fläche des Versammlungsortes zulässigen Teilnehmendenzahl bei der Durchführung der Versammlung hervorgehen. Die Versammlungsbehörde kann die Vorlage dieses Schutz- und Hygienekonzepts von der die Versammlung veranstaltenden Person verlangen und beim zuständigen Gesundheitsamt eine infektionsschutzrechtliche Bewertung des Konzepts einholen. Bei der Durchführung der Versammlungen ist die Einhaltung des Schutz- und Hygienekonzepts von der Versammlungsleitung sicherzustellen.\n\n(3) Zugelassene Krankenhäuser dürfen planbare Aufnahmen, Operationen und Eingriffe unter der Voraussetzung durchführen, dass Reservierungs- und Freihaltevorgaben eingehalten werden und die Rückkehr in einen Krisenmodus wegen einer Verschärfung der Pandemielage jederzeit kurzfristig umgesetzt werden kann. Das Nähere hierzu und zu Besuchsregelungen bestimmt die für Gesundheit zuständige Senatsverwaltung durch Rechtsverordnung nach Maßgabe des § 32 Satz 1 des Infektionsschutzgesetzes.\n\n(3a) Im Bereich der Eingliederungshilfe und der Sozialhilfe kann die für Soziales zuständige Senatsverwaltung Regelungen durch Rechtsverordnung nach Maßgabe des § 32 Satz 1 des Infektionsschutzgesetzes bestimmen, die eine Grundversorgung der Leistungsberechtigten sicherstellen. Leistungserbringer mit Vereinbarungen nach § 123 Neuntes Buch Sozialgesetzbuch oder § 75 Zwölftes Buch Sozialgesetzbuch - Sozialhilfe - (Artikel 1 des Gesetzes vom 27. Dezember 2003, BGBl. I S. 3022, 3023), das zuletzt durch Artikel 11 des Gesetzes vom 14. Dezember 2019 (BGBl. I S. 2789) geändert worden ist, sind zur Abwendung von Gefahren für Mitarbeitende und Leistungsberechtigte befugt, das Personal abweichend von den Leistungsvereinbarungen, aber im inhaltlichen Rahmen des Leistungsbereichs, einzusetzen. Die Grundversorgung der Leistungsberechtigten ist sicherzustellen.\n\n(4) Bei der Öffnung von Verkaufsstellen, Kaufhäusern und Einkaufszentren (Malls) gilt für die Steuerung des Zutritts und zur Sicherung des Mindestabstandes ein Richtwert für die maximal zulässige Anzahl von Kundinnen und Kunden je Verkaufsfläche oder Geschäftsraum. Bei Geschäften mit einer Verkaufsfläche von bis zu 800 Quadratmetern gilt ein Richtwert von insgesamt höchstens einer Kundin oder einem Kunden pro 10 Quadratmetern Verkaufsfläche. Bei Geschäften mit einer Verkaufsfläche ab 801 Quadratmetern insgesamt gilt auf einer Fläche von 800 Quadratmetern ein Richtwert von höchstens einer Kundin oder einem Kunden pro 10 Quadratmetern Verkaufsfläche und auf der 800 Quadratmeter übersteigenden Fläche von höchstens einer Kundin oder einem Kunden pro 20 Quadratmeter Verkaufsfläche. Für Einkaufszentren ist die jeweilige Gesamtverkaufsfläche maßgeblich. Unterschreiten die Verkaufsfläche oder der Geschäftsraum eine Größe von 20 Quadratmetern, darf jeweils höchstens eine Kundin oder ein Kunde eingelassen werden. Aufenthaltsanreize dürfen nicht geschaffen werden. Insbesondere sind die Verkehrsflächen von Verkaufsständen freizuhalten. § 1 Absatz 4 gilt entsprechend.\n\n(5) Auf nach dieser Verordnung zulässigen Veranstaltungen sind die Bestuhlung und Anordnung der Tische so vorzunehmen, dass zwischen Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, ein Mindestabstand von 1,5 Metern eingehalten wird oder ein ausreichender Infektionsschutz durch andere Schutzmaßnahmen oder Schutzvorrichtungen zur Verringerung der Ausbreitung übertragungsfähiger Tröpfchenpartikel gewährleistet werden kann. Abweichend von Satz 1 sowie § 1 Absatz 2 Satz 1 dürfen Gruppen von bis zu zwei Personen mit weniger als 1,5 Metern Abstand untereinander platziert werden. Bei Veranstaltungen im Freien kann der Mindestabstand nach Satz 1 unterschritten werden, sofern der Schutz vor Tröpfcheninfektionen und Aerosolen sichergestellt ist.\n\n(6) In Kantinen dürfen Speisen und Getränke nur an Tischen sowie sitzend an Theken und Tresen verzehrt werden. Die Bestuhlung und Anordnung der Tische ist so vorzunehmen, dass zwischen Personen, die nicht unter die Ausnahme des § 1 Absatz 3 fallen, ein Mindestabstand von 1,5 Metern eingehalten wird. Abweichend von Satz 2 sowie § 1 Absatz 2 Satz 1 dürfen Gruppen von bis zu zwei Personen mit weniger als 1,5 Metern Abstand untereinander an einem Tisch sitzen. Im Freien kann der Mindestabstand nach Satz 2 unterschritten werden, sofern der Schutz vor Tröpfcheninfektionen und Aerosolen sichergestellt ist. Im Abstandsbereich dürfen sich keine Personen aufhalten. Ein verstärktes Reinigungs- und Desinfektionsregime ist sicherzustellen.\n\n(7) Sport darf vorbehaltlich des Satzes 2 nur alleine oder mit einer anderen Person kontaktfrei und unter Einhaltung der Abstandsregelungen nach § 1 Absatz 2 erfolgen. Für folgende Personengruppen gilt die Beschränkung des Satz 1 nicht:\na) für den Personenkreis gemäß § 1 Absatz 3,\nb) für Bundes- und Landeskaderathletinnen und -athleten, Profiligen und Berufssportlerinnen und Berufssportler,\nc) für Kinder im Alter von bis zu 12 Jahren, wenn der Sport im Freien in festen Gruppen von maximal 10 anwesenden Personen zuzüglich einer betreuenden Person ausgeübt wird und\nd) für ärztlich verordneten Rehabilitationssport oder ärztlich verordnetes Funktionstraining im Sinne des § 64 Absatz 1 Nummer 3 und 4 des Neunten Buches Sozialgesetzbuch vom 23. Dezember 2016 (BGBl. I S. 3234), das zuletzt durch Artikel 3 Absatz 6 des Gesetzes vom 9. Oktober 2020 (BGBl. I S. 2075) geändert worden ist, in festen Gruppen von bis zu höchstens zehn Personen zuzüglich einer übungsleitenden Person; bei besonderen im Einzelfall zu begründenden Härtefällen ist die Beteiligung weiterer Personen zulässig, soweit dies zwingend notwendig ist, um den Teilnehmenden die Ausübung des Rehabilitationssports oder Funktionstrainings zu ermöglichen.\n\nDie Verantwortlichen sind verpflichtet vor Beginn der Sporteinheit auf die Einhaltung des Schutz- und Hygienekonzepts nach § 2 Absatz 1 hinzuweisen und für dessen Umsetzung Sorge zu tragen. Regelungen über den Sport an öffentlichen Schulen und Schulen in freier Trägerschaft, an Einrichtungen der Berufsbildung sowie als studienbezogener Lehrbetrieb der Hochschulen gehen diesem Absatz und Absatz 7a vor.\n\n(7a) Gedeckte Sportanlagen dürfen nur geöffnet werden, soweit dies erforderlich ist\na) für den Sport des in § 5 Absatz 7 Satz 2 Buchstabe b genannten Personenkreises,\nb) für den Pferdesport in dem unter Tierschutzgesichtspunkten zwingend erforderlichen Umfang,\nc) für therapeutische Behandlungen sowie Nutzungen nach Maßgabe des Absatz 7 Satz 2 Buchstabe d.\n\nAnsonsten bleiben sie geschlossen.\n\n(8) Der professionelle sportliche Wettkampfbetrieb in der Bundesliga und den internationalen Ligen sowie vergleichbaren professionellen Wettkampfsystemen ist zulässig, soweit er im Rahmen eines Nutzungs- und Hygienekonzeptes des jeweiligen Sportfachverbandes stattfindet. Zuschauende sind untersagt. Satz 2 gilt nicht für die für den Spielbetrieb erforderlichen Personen.\n\n(9) Schwimmbäder dürfen ausschließlich für die Nutzung durch Bundes- und Landeskaderathletinnen und -athleten, Profiligen und Berufssportlerinnen und -sportler, für den Sport als Unterrichtsfach an öffentlichen Schulen und Schulen in freier Trägerschaft, an Einrichtungen der Berufsbildung und als studienbezogener Lehrbetrieb der Hochschulen, für therapeutische Behandlung sowie Nutzungen nach Maßgabe des Absatz 7 Satz 2 Buchstabe d geöffnet werden. Frei- und Strandbäder bleiben geschlossen.\n\n(10) Im Bereich der Kindertagesförderung kann die für Jugend und Familie zuständige Senatsverwaltung in Fällen eines auf Grund der Infektionslage eingeschränkten Einsatzes von Fachpersonal in den Einrichtungen Näheres bestimmen, um dennoch die Betreuungsumfänge unter Beachtung der Hygienevorgaben nach dem Kindertagesförderungsgesetz vom 23. Juni 2005 (GVBl. S. 322), das zuletzt durch Artikel 1 des Gesetzes vom 11. Juni 2020 (GVBl. S. 535) geändert worden ist, erfüllen zu können.\n\n(11) (aufgehoben)\n\n(12) Staatliche, private und konfessionelle Hochschulen einschließlich ihrer Einrichtungen dürfen bis zum 31. März 2021 nicht für den Publikumsverkehr geöffnet werden. Die Hochschulen führen ihren Lehrbetrieb im Wintersemester 2020/2021 ab 2. November 2020 grundsätzlich mit Online-Formaten und nicht im Präsenzlehrbetrieb durch. Praxisformate, die nicht digital durchführbar sind, und Prüfungen dürfen unter Beachtung der grundsätzlichen Pflichten, der Schutz- und Hygieneregeln nach Teil 1 sowie der jeweils in den Hochschulen geltenden besonderen Bestimmungen in Präsenzform durchgeführt werden. Zulässig nach Satz 3 sind insbesondere\n1. Praxisformate, die spezielle Labor- und Arbeitsräume an den Hochschulen erfordern,\n2. praktischer Unterricht in medizinisch-klinischen Studiengängen,\n3. künstlerischer Unterricht,\n4. sportpraktische Übungen und\n5. Präsenzformate zur Einführung von Studienanfängerinnen und Studienanfängern.\n\nIn Praxisformaten nach Satz 4 soll die maximale Anzahl von 25 teilnehmenden Studierenden grundsätzlich nicht überschritten werden. In begründeten Fällen können die Hochschulen Personen abweichend von Satz 1 begrenzten Zutritt gestatten. Satz 1 gilt nicht für wissenschaftliche Bibliotheken und den Botanischen Garten.",
}


def test_():
    first_section = Section.from_dict(first, "")
    section_section = Section.from_dict(second, "")
    breakpoint()
