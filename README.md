# Dómagreining  alpha útgáfa 1.0

**Eftir Magnús Smára** | [www.smarason.is](https://www.smarason.is)

## Um verkefnið

Dómagreining er opinn hugbúnaður sem gerir notendum kleift að hlaða upp PDF eða TXT skjölum af íslenskum dómum og greina þá með hjálp GPT-4. Forritið dregur út lykilupplýsingar úr dómnum og skilar skipulagðri greiningu.

## Eiginleikar

- Tekur við PDF og TXT skjölum
- Textaútdráttur úr PDF skjölum
- Greining dóma með GPT-4o (krefst OpenAI API lykils)
- Skipulögð svörun með 8 lykilþáttum
- Hægt er að hlaða niður greiningunni

## Þróun

-Fjölga mögulegum módelum
   -Anthropic
   -Google
   -Ollama

-Lengra samtal eftir greininguna



## Uppsetning

1. Klónaðu þetta geymslu (repository):
   ```
   git clone https://github.com/yourusername/doma-reifari.git
   cd doma-reifari
   ```

2. Settu upp virtual environment (valfrjálst en mælt með):
   ```
   python -m venv venv
   source venv/bin/activate  # Á Windows: venv\Scripts\activate
   ```

3. Settu upp nauðsynleg pakka:
   ```
   pip install -r requirements.txt
   ```

4. Fáðu OpenAI API lykil:
   - Farðu á [OpenAI's website](https://openai.com/api/) og búðu til reikning eða skráðu þig inn
   - Búðu til nýjan API lykil í stjórnborðinu þínu
   - Geymdu API lykilinn á öruggum stað - þú munt nota hann þegar þú keyrir appið

## Notkun

1. Keyrðu Streamlit appið:
   ```
   streamlit run doma_reifari.py
   ```

2. Opnaðu vafra og farðu á slóðina sem birtist í skipanalínunni (venjulega `http://localhost:8501`).

3. Sláðu inn OpenAI API lykilinn þinn þegar beðið er um hann.

4. Hladdu upp PDF eða TXT skjali af íslenskum dómi.

5. Smelltu á "Greina mál" hnappinn til að hefja greininguna.

6. Skoðaðu niðurstöðurnar og haltu niður fullri greiningu ef þú vilt.

## API lykill og öryggisatriði

- Þetta app notar OpenAI API og krefst þess að þú notir þinn eigin API lykil.
- API lykillinn þinn er notaður beint í appinu og er ekki geymdur.
- Þú berð ábyrgð á notkun API lykilsins þíns og öllum kostnaði sem fylgir notkun hans.
- Vinsamlegast lestu og fylgdu [OpenAI's use policies](https://openai.com/policies/usage-policies).

## Framlag

Framlög er velkomið! Vinsamlegast opnið málefni (issue) áður en þið sendið pull request.

## Leyfi

Þetta verkefni er undir MIT leyfi. Sjá [LICENSE](LICENSE) skrána fyrir nánari upplýsingar.

## Ábyrgð

Þetta verkefni er veitt "eins og það er", án nokkurrar ábyrgðar. Notkun er alfarið á eigin ábyrgð. Höfundar eða þátttakendur bera ekki ábyrgð á notkun eða afleiðingum notkunar þessa hugbúnaðar.

## Tengiliður

Magnús Smári - [www.smarason.is](https://www.smarason.is)

Verkefnishlekkur: [https://github.com/yourusername/doma-reifari](https://github.com/yourusername/doma-reifari)](https://github.com/Magnussmari/Domagreining/)

---

**Athugið:** Notkun er alfarið á eigin ábyrgð!
