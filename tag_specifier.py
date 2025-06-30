import pandas as pd
import io
import re

# The provided text data
pos_text_data = """
NO TAG PART OF SPEECH
1 Ap Adjective, predicative
2 Apc Adjective, predicative, comparative or superlative
3 Aps Adjective, predicative, second comparative
4 Aq Adjective, qualificator (attributive)
5 Aq-dfd Adjective, qualificator, dual, feminine, dative
6 Aq-dfn Adjective, qualificator, dual, feminine, nominative
7 Aq-p Adjective, qualificator, plural
8 Aq-pfd Adjective, qualificator, plural, feminine, dative
9 Aq-pfg Adjective, qualificator, plural, feminine, genitive
10 Aq-pfn Adjective, qualificator, plural, feminine, nominative
11 Aq-pfv Adjective, qualificator, plural, feminine, vocative
12 Aq-pmd Adjective, qualificator, plural, masculine, dative
13 Aq-pmg Adjective, qualificator, plural, masculine, genitive
14 Aq-pmn Adjective, qualificator, plural, masculine, nominative
15 Aq-pmv Adjective, qualificator, plural, masculine, vocative
16 Aq-s Adjective, qualificator, singular
17 Aq-sfd Adjective, qualificator, singular, feminine, dative
18 Aq-sfg Adjective, qualificator, singular, feminine, genitive
19 Aq-sfn Adjective, qualificator, singular, feminine, nominative
20 Aq-sfv Adjective, qualificator, singular, feminine, vocative
21 Aq-smd Adjective, qualificator, singular, masculine, dative
22 Aq-smg Adjective, qualificator, singular,masculine, genitive
23 Aq-smn Adjective, qualificator, singular, masculine, nominative
24 Aq-smv Adjective, qualificator, singular, masculine, vocative
25 Ar Adjective, preposed
26 Av Adjective, verbal
27 Cc Conjunction, coordinate
28 Cs Conjunction, subordinate
29 Cs+Qq Fused Form: subordinating conjunction fused with
interrogative verbal particle
30 Csw Conjunction, subordinate with copula
31 Dd Determiner, demonstrative
32 Dp1p Determiner, possessive, first person plural
33 Dp2p Determiner, possessive, second person plural
34 Dp3p Determiner, possessive,third person plural
35 Dp1s Determiner, possessive,first person singular
36 Dp2s Determiner, possessive, second person singular
37 Dp3sf Determiner, possessive, third person singular, feminine
38 Dp3sm Determiner, possessive, third person singular, masculine
39 Dq Determiner, quantifier
40 Fb Punctuation, hyphen/ underscore/ dash/ ellipsis/ parentheses
41 Fe Punctuation, sentence final (full stop)
42 Fg Punctuation, question mark
43 Fi Punctuation, sentence internal (comma, colon, semi-colon)
44 Fq Punctuation, quote (opening quotation mark)
45 Fu Punctuation, exclamation mark
46 Fz Punctuation, quote (closing quotation mark)
47 I Interjection
48 Mc Numeral, cardinal
49 Mn Numeral , symbolic
50 Mo Numeral, ordinal
51 Mr Numeral, roman
52 Ms Numeral, operator
53 Ncdfd Noun, common, dual, feminine, dative
54 Ncdfde Noun, common, dual, feminine, dative, emphatic
55 Ncdfn Noun, common, dual, feminine, nominative
56 Ncdfne Noun, common, plural, feminine, nominative, emphatic
57 Ncpfd Noun, common, plural, feminine, dative
58 Ncpfde Noun, common, plural, feminine, dative, emphatic
59 Ncpfg Noun, common, plural, feminine, genitive
60 Ncpfge Noun, common, plural, feminine, genitive, emphatic
61 Ncpfn Noun, common, plural, feminine, nominative
62 Ncpfne Noun, common, plural, feminine, nominative, emphatic
63 Ncpfv Noun, common, plural, feminine, vocative
64 Ncpmd Noun, common, plural, masculine, dative
65 Ncpmde Noun, common, plural, masculine, dative, emphatic
66 Ncpmg Noun, common, plural, masculine, genitive
67 Ncpmge Noun, common, plural, masculine, genitive, emphatic
68 Ncpmn Noun, common, plural, masculine, nominative
69 Ncpmne Noun, common, plural, masculine, nominative, emphatic
70 Ncpmv Noun, common, plural, masculine, vocative
71 Ncsfd Noun, common, singular, feminine, dative
72 Ncsfde Noun, common, singular, feminine, dative, emphatic
73 Ncsfg Noun, common, singular, feminine, genitive
74 Ncsfge Noun, common, singular, feminine, genitive, emphatic
75 Ncsfn Noun, common, singular, feminine, nominative
76 Ncsfn+Pr1s Fused Form: singular feminine noun fused with first person
singular prepositional pronoun
77 Ncsfne Noun, common, singular, feminine, nominative, emphatic
78 Ncsfv Noun, common, singular, feminine, vocative
79 Ncsmd Noun, common, singular, masculine, dative
80 Ncsmde Noun, common, singular, masculine, dative, emphatic
81 Ncsmg Noun, common, singular, masculine, genitive
82 Ncsmge Noun, common, singular, masculine, genitive, emphatic
83 Ncsmn Noun, common, singular, masculine, nominative
84 Ncsmn+Pr1s Fused Form: singular masculine noun fused with first person
singular prepositional pronoun
85 Ncsmne Noun, common, singular, masculine, nominative, emphatic
86 Ncsmv Noun, common, singular, masculine, vocative
87 Nf Noun, fossilised lexeme
88 Nf---e Noun, fossilised lexeme, emphatic
89 Nn Noun, name (surname)
90 Nn-fd Noun, name, feminine, dative
91 Nn-fg Noun, name, feminine, genitive
92 Nn-fn Noun, name, feminine, nominative
93 Nn-fv Noun, name, feminine, vocative
94 Nn-md Noun, name, masculine, dative
95 Nn-mg Noun, name, masculine, genitive
96 Nn-mn Noun, name, masculine, nominative
97 Nn-mv Noun, name, masculine, vocative
98 Nt Noun, toponym
99 Nv Noun, verbal
100 Nv---e Noun, verbal, emphatic
101 Pd Pronoun, demonstrative
102 Pn Pronoun, numerical
103 Pp1p Pronoun, personal, first person plural
104 Pp1p--e Pronoun, personal, first person plural, emphatic
105 Pp2p Pronoun, personal, second person plural
106 Pp2p--e Pronoun, personal, second person plural, emphatic
107 Pp3p Pronoun, personal, third person plural
108 Pp3p--e Pronoun, personal, third person plural, emphatic
109 Pp3p-n Pronoun, personal, third person plural, nominative
110 Pp3p-ne Pronoun, personal, third person plural, nominative, emphatic
111 Pp1s Pronoun, personal, first person singular
112 Pp1s--e Pronoun, personal, first person singular, emphatic
113 Pp2s Pronoun, personal, second person singular
114 Pp2s--e Pronoun, personal, second person singular, emphatic
115 Pp3sf Pronoun, personal, third person singular, feminine
116 Pp3sf-e Pronoun, personal, third person singular, feminine, emphatic
117 Pp3sfn Pronoun, personal, third person singular, feminine, nominative
118 Pp3sfne Pronoun, personal, third person singular, feminine, nominative,
emphatic
119 Pp3sm Pronoun, personal, third person singular, masculine
120 Pp3sm-e Pronoun, personal, third person singular, masculine, emphatic
121 Pp3smn Pronoun, personal, third person singular, masculine,
nominative
122 Pp3smne Pronoun, personal, third person singular, masculine,
123 Pr1p nominative, emphatic
Pronoun, prepositional, first person plural
124 Pr1p--e Pronoun, prepositional, first person plural, emphatic
125 Pr2p Pronoun, prepositional, second person plural
126 Pr2p--e Pronoun, prepositional, second person plural, emphatic
127 Pr3p Pronoun, prepositional, third person plural
128 Pr3p--e Pronoun, prepositional, third person plural, emphatic
129 Pr1s Pronoun, prepositional, first person singular
130 Pr1s--e Pronoun, prepositional, first person singular, emphatic
131 Pr2s Pronoun, prepositional, second person singular
132 Pr2s--e Pronoun, prepositional, second person singular, emphatic
133 Pr3sf Pronoun, prepositional, third person singular, feminine
134 Pr3sf-e Pronoun, prepositional, third person singular, feminine,
emphatic
135 Pr3sm Pronoun, prepositional, third person masculine
136 Pr3sm-e Pronoun, prepositional, third person masculine, emphatic
137 Px Pronoun, reflexive
138 Qa Verbal particle, affirmative
139 Qa+Q--s Fused Form : affirmative verbal particle fused with past tense
verbal particle
140 Qn Verbal particle, negative complementiser
141 Qnm Verbal particle, negative complementiser, imperative
142 Qnr Verbal particle, negative complementiser, relative
143 Qq Verbal particle, interrogative/ dependent clause marker
144 Qq+Q--s Fused Form: interrogative verbal particle fused with past tense
verbal particle
145 Q-r Verbal particle, relative
146 Q-s Verbal particle, subjunctive
147 Q--s Verbal particle, past tense
148 Rg Adverb, general
149 Rg+Cc Fused Form: adverb fused with coordinating conjunction
150 Rs Adverb, spatial
151 Rt Adverb, temporal
152 Sa Adposition, aspectual
153 Sap1p Adposition, aspectual with possessive determiner, first person
plural
154 Sap2p Adposition, aspectual with possessive determiner, second
person plural
155 Sap3p Adposition, aspectual with possessive determiner, third person
plural
156 Sap1s Adposition, aspectual with possessive determiner, first person
singular
157 Sap2s Adposition, aspectual with possessive determiner, second
person singular
157 Sap2s Adposition, aspectual with possessive determiner, second
person singular
158 Sap3sf Adposition, aspectual with possessive determiner, third person
singular, feminine
159 Sap3sm Adposition, aspectual with possessive determiner, third person
singular, masculine
160 Sp Adposition, preposition
161 Sp+Dp2s Fused Form: preposition fused with second person singular
possessive pronoun
162 Sp+Q-r Fused Form: preposition fused with relative verbal particle
163 Spa-p Adposition, preposition with article, plural
164 Spa-s Adposition, preposition with article, singular
165 Spp1p Adposition, preposition with possessive determiner, first
person plural
166 Spp2p Adposition, preposition with possessive determiner, second
person plural
167 Spp3p Adposition, preposition with possessive determiner, third
person plural
168 Spp1s Adposition, preposition with possessive determiner, first
person singular
169 Spp2s Adposition, preposition with possessive determiner, second
person singular
170 Spp3sf Adposition, preposition with possessive determiner, third
person singular, feminine
171 Spp3sm Adposition, preposition with possessive determiner, third
person singular, masculine
172 Spr Adposition, preposition with relative particle
173 Spv Adposition, preposition fused with verbal particle
174 Tdp Article, definite, plural
175 Tdpf Article, definite, plural, feminine
176 Tdpfg Article, definite, plural, feminine, genitive
177 Tdp-g Article, definite, plural, genitive
178 Tdpm Article, definite, plural, masculine
179 Tdpmg Article, definite, plural, masculine, genitive
180 Tds Article, definite, singular
181 Tdsf Article, definite, singular, feminine
182 Tdsfg Article, definite, singular, feminine, genitive
183 Tds-g Article, definite, singular, genitive
184 Tdsm Article, definite, singular, masculine
185 Tdsmg Article, definite, singular, masculine, genitive
186 Ua Unique membership class, adverbial
187 Uc Unique membership class, comparative/superlative
188 Uf Unique membership class, fixed copular multi-word
expressions
189 Ug Unique membership class, agreement
190 Um Unique membership class, complementiser (phrasal)
191 Uo Unique membership class, morphophonemic
192 Up Unique membership class, patronym
193 Uq Unique membership class, question words
194 Uq+V-p--d Fused Form: question word fused with present dependent verb
34Scottish Gaelic PoS Annotation Guidelines Manual
195 Uv Unique membership class, vocative
196 V-f Verb, future/ present habitual
197 V-f--d Verb, future/ present habitual, dependent
198 V-f--r Verb, future/ present habitual, relative
199 V-f0 Verb, future/ present habitual, impersonal/ passive
200 V-f0-d Verb, future/ present habitual, impersonal/ passive, dependent
201 V-h Verb, past habitual/ conditional
202 V-h--d Verb, past habitual/ conditional, dependent
203 V-h0 Verb, past habitual/ conditional, passive
204 V-h0-d Verb, past habitual/ conditional, passive, dependent
205 V-h1p Verb, past habitual/ conditional, first person plural
206 V-h1pd Verb, past habitual/ conditional, first person plural, dependent
207 V-h1s Verb, past habitual/ conditional, first person singular
208 V-h1sd Verb, past habitual/ conditional, first person singular,
dependent
209 V-h1sde Verb, past habitual/ conditional, first person singular,
dependent, emphatic
210 V-h1s-e Verb, past habitual/ conditional, first person singular, emphatic
211 Vm-1p Verb, imperative, first person plural
212 Vm-2p Verb, imperative, second person plural
213 Vm-3 Verb, imperative, third person (singular or plural)
214 Vm-1s Verb, imperative, first person singular
215 Vm-2s Verb, imperative, second person singular
216 V-p Verb, present
217 V-p--d Verb, present, dependent
218 V-p0 Verb, present, passive
219 V-p0-d Verb, present, passive, dependent
220 V-s Verb, past
221 V-s--d Verb, past, dependent
222 V-s0 Verb, past, passive
223 V-s0-d Verb, past, passive, dependent
224 Wpdia Copula, present/ future, dependent, indicative, affirmative
225 Wpdin Copula, present/ future, dependent, indicative, negative
226 Wpdqa Copula, present/ future, dependent, interrogative, affirmative
227 Wpdqn Copula, present/ future, dependent, interrogative, negative
228 Wp-i Copula, present/ future, indicative
229 Wp-i-3 Copula, present/ future, indicative, third person pronoun
230 Wp-in Copula, present/ future, indicative, negative
231 Wp-i-x Copula, present/ future, indicative, existential
232 Wpr Copula, present/ future, relative
233 Ws Copula, past/ conditional
234 Xa Residual, acronym
235 Xd Residual, date
236 Xe Residual, e-mail address
237 Xf Residual, foreign
238 Xfe Residual, foreign, English
239 Xsc Resdiual, spoken, communicator
240 Xsev Residual, spoken, event
241 Xsi Residual, spoken, incomplete
242 Xsp Residual, spoken, phonetic element
243 Xw Residual, website address
244 Xx Residual, unknown/ unintelligible
245 Xy Residual, symbol
246 Y Abbreviation"""

# Using io.StringIO to simulate reading from a file
data_io = io.StringIO(pos_text_data)

# Skip the first line (header "NO TAG PART OF SPEECH")
data_lines = data_io.readlines()[1:]

parsed_data = []

# Regex to capture the tag and the rest of the description
# It looks for a number at the start, then captures the tag (alphanumeric, hyphens, plus signs),
# and then captures everything else until the end of the line.
# It also handles multi-line descriptions for "Fused Form" by joining them.
tag_pattern = re.compile(r'^\s*\d+\s+([A-Za-z0-9+-]+)\s+(.*)')

current_tag = None
current_description_lines = []

for line in data_lines:
    line = line.strip()

    # Skip lines that are just page numbers/headers (like "34Scottish Gaelic PoS Annotation Guidelines Manual")
    # or empty lines.
    if not line or re.match(r'^\d+Scottish Gaelic PoS Annotation Guidelines Manual', line):
        continue

    match = tag_pattern.match(line)
    if match:
        # If a new tag line is found, process the previous accumulated description
        if current_tag:
            parsed_data.append({
                'TAG': current_tag,
                'DESCRIPTION': ' '.join(current_description_lines).replace(' \n', ' ').strip()
            })

        # Start new entry
        current_tag = match.group(1).strip()
        current_description_lines = [match.group(2).strip()]
    else:
        # This line is a continuation of the description for the current tag
        if current_description_lines:
            current_description_lines.append(line)
        # If it's a continuation but no current_tag, it's an unparseable line, skip.

# Add the last entry after the loop finishes
if current_tag:
    parsed_data.append({
        'TAG': current_tag,
        'DESCRIPTION': ' '.join(current_description_lines).replace(' \n', ' ').strip()
    })

# Create a DataFrame
df = pd.DataFrame(parsed_data)

# Convert DataFrame to CSV string
csv_output = df.to_csv(index=False)

# Print the CSV output
print(csv_output)
