import re

raw_data = """
1: Company,Year,Role,Experience,Salary_LPA,Skill,Domain,Hiring_Type
2: Zoho,2018,Software Engineer,2,6.5,Java,Product,Campus
3: TCS,2018,Systems Analyst,4,8.2,Python,IT Services,Lateral
4: HCL,2018,Junior Developer,1,4.8,C++,IT Services,Campus
5: Infosys,2018,Technology Analyst,3,9.1,Java,IT Services,Lateral
6: Wipro,2018,Software Engineer,2,6.0,JavaScript,IT Services,Campus
7: Accenture,2018,Associate,1,5.5,SQL,Consulting,Campus
8: Zoho,2018,Senior Developer,5,14.0,Python,Product,Lateral
9: TCS,2018,Project Lead,7,16.5,Java,IT Services,Lateral
10: HCL,2018,Software Engineer,2,6.2,JavaScript,IT Services,Campus
11: Infosys,2018,Senior Systems Engineer,4,10.5,Python,IT Services,Lateral
12: Wipro,2018,Project Manager,8,22.0,Java,IT Services,Lateral
13: Accenture,2018,Analyst,2,7.0,SQL,Consulting,Lateral
14: Zoho,2018,QA Engineer,3,8.0,Selenium,Product,Lateral
15: TCS,2018,Business Analyst,5,12.0,SQL,IT Services,Lateral
16: HCL,2018,DevOps Engineer,4,11.5,Docker,IT Services,Lateral
17: Infosys,2018,Junior Developer,1,4.5,C++,IT Services,Campus
18: Wipro,2018,Data Analyst,3,9.5,Python,IT Services,Lateral
19: Accenture,2018,Technology Consultant,6,18.0,Java,Consulting,Lateral
20: Zoho,2018,Product Manager,7,20.0,Agile,Product,Lateral
21: TCS,2018,Software Engineer,2,7.0,JavaScript,IT Services,Campus
22: HCL,2018,QA Engineer,2,6.5,Selenium,IT Services,Campus
23: Infosys,2018,Cloud Engineer,5,13.5,AWS,IT Services,Lateral
24: Wipro,2018,Junior Analyst,1,4.2,SQL,IT Services,Campus
25: Accenture,2018,Senior Analyst,4,11.0,Python,Consulting,Lateral
26: Zoho,2019,Software Engineer,2,7.0,Java,Product,Campus
27: TCS,2019,Systems Analyst,5,9.5,Python,IT Services,Lateral
28: HCL,2019,Junior Developer,1,5.0,C++,IT Services,Campus
29: Infosys,2019,Technology Analyst,3,9.8,Java,IT Services,Lateral
30: Wipro,2019,Software Engineer,2,6.5,JavaScript,IT Services,Campus
31: Accenture,2019,Associate,1,6.0,SQL,Consulting,Campus
32: Zoho,2019,Senior Developer,6,16.0,Python,Product,Lateral
33: TCS,2019,Project Lead,8,18.0,Java,IT Services,Lateral
34: HCL,2019,Software Engineer,2,6.8,JavaScript,IT Services,Campus
35: Infosys,2019,Senior Systems Engineer,4,11.5,Python,IT Services,Lateral
36: Wipro,2019,Project Manager,8,23.0,Java,IT Services,Lateral
37: Accenture,2019,Analyst,2,7.5,SQL,Consulting,Lateral
38: Zoho,2019,QA Engineer,3,9.0,Selenium,Product,Lateral
39: TCS,2019,Business Analyst,5,13.0,SQL,IT Services,Lateral
40: HCL,2019,DevOps Engineer,4,12.5,Docker,IT Services,Lateral
41: Infosys,2019,Junior Developer,1,5.0,C++,IT Services,Campus
42: Wipro,2019,Data Analyst,3,10.5,Python,IT Services,Lateral
43: Accenture,2019,Technology Consultant,6,19.0,Java,Consulting,Lateral
44: Zoho,2019,Product Manager,8,22.0,Agile,Product,Lateral
45: TCS,2019,Software Engineer,2,7.5,JavaScript,IT Services,Campus
46: HCL,2019,QA Engineer,2,7.0,Selenium,IT Services,Campus
47: Infosys,2019,Cloud Engineer,5,15.0,AWS,IT Services,Lateral
48: Wipro,2019,Junior Analyst,1,4.5,SQL,IT Services,Campus
49: Accenture,2019,Senior Analyst,4,12.5,Python,Consulting,Lateral
50: Zoho,2019,ML Engineer,4,18.0,TensorFlow,Product,Lateral
51: TCS,2019,Data Scientist,5,17.0,Python,IT Services,Lateral
52: HCL,2019,Cloud Architect,7,24.0,AWS,IT Services,Lateral
53: Infosys,2019,Senior Developer,5,14.0,Java,IT Services,Lateral
54: Wipro,2019,Network Engineer,3,9.0,Cisco,IT Services,Lateral
55: Accenture,2019,Manager,9,32.0,Agile,Consulting,Lateral
56: Zoho,2020,Software Engineer,2,7.5,Java,Product,Campus
57: TCS,2020,Systems Analyst,5,10.0,Python,IT Services,Lateral
58: HCL,2020,Junior Developer,1,5.2,C++,IT Services,Campus
59: Infosys,2020,Technology Analyst,3,10.0,Java,IT Services,Lateral
60: Wipro,2020,Software Engineer,2,6.8,JavaScript,IT Services,Campus
61: Accenture,2020,Associate,1,6.2,SQL,Consulting,Campus
62: Zoho,2020,Senior Developer,6,17.5,Python,Product,Lateral
63: TCS,2020,Project Lead,8,19.5,Java,IT Services,Lateral
64: HCL,2020,Software Engineer,2,7.0,JavaScript,IT Services,Campus
65: Infosys,2020,Senior Systems Engineer,4,12.0,Python,IT Services,Lateral
66: Wipro,2020,Project Manager,9,24.0,Java,IT Services,Lateral
67: Accenture,2020,Analyst,2,8.0,SQL,Consulting,Lateral
68: Zoho,2020,QA Engineer,3,9.5,Selenium,Product,Lateral
69: TCS,2020,Business Analyst,5,13.5,SQL,IT Services,Lateral
70: HCL,2020,DevOps Engineer,4,13.5,Docker,IT Services,Lateral
71: Infosys,2020,Junior Developer,1,5.2,C++,IT Services,Campus
72: Wipro,2020,Data Analyst,3,11.0,Python,IT Services,Lateral
73: Accenture,2020,Technology Consultant,6,20.0,Java,Consulting,Lateral
74: Zoho,2020,Product Manager,8,24.0,Agile,Product,Lateral
75: TCS,2020,Software Engineer,2,8.0,JavaScript,IT Services,Campus
76: HCL,2020,QA Engineer,2,7.5,Selenium,IT Services,Campus
77: Infosys,2020,Cloud Engineer,5,16.0,AWS,IT Services,Lateral
78: Wipro,2020,Junior Analyst,1,4.8,SQL,IT Services,Campus
79: Accenture,2020,Senior Analyst,4,13.5,Python,Consulting,Lateral
80: Zoho,2020,ML Engineer,4,20.0,TensorFlow,Product,Lateral
81: TCS,2020,Data Scientist,5,18.5,Python,IT Services,Lateral
82: HCL,2020,Cloud Architect,7,25.5,AWS,IT Services,Lateral
83: Infosys,2020,Senior Developer,5,15.0,Java,IT Services,Lateral
84: Wipro,2020,Network Engineer,3,9.5,Cisco,IT Services,Lateral
85: Accenture,2020,Manager,9,34.0,Agile,Consulting,Lateral
86: Zoho,2020,Frontend Developer,3,11.0,React,Product,Lateral
87: TCS,2020,Security Analyst,4,13.0,Cybersecurity,IT Services,Lateral
88: HCL,2020,SAP Consultant,6,19.0,SAP,IT Services,Lateral
89: Infosys,2020,Scrum Master,5,16.0,Agile,IT Services,Lateral
90: Wipro,2020,Full Stack Developer,3,12.0,Node.js,IT Services,Lateral
91: Accenture,2020,Data Engineer,4,15.5,Spark,Consulting,Lateral
92: Zoho,2021,Software Engineer,2,9.0,Java,Product,Campus
93: TCS,2021,Systems Analyst,5,11.0,Python,IT Services,Lateral
94: HCL,2021,Junior Developer,1,5.8,C++,IT Services,Campus
95: Infosys,2021,Technology Analyst,3,11.0,Java,IT Services,Lateral
96: Wipro,2021,Software Engineer,2,7.5,JavaScript,IT Services,Campus
97: Accenture,2021,Associate,1,7.0,SQL,Consulting,Campus
98: Zoho,2021,Senior Developer,6,20.0,Python,Product,Lateral
99: TCS,2021,Project Lead,8,21.0,Java,IT Services,Lateral
100: HCL,2021,Software Engineer,2,8.0,JavaScript,IT Services,Campus
101: Infosys,2021,Senior Systems Engineer,4,13.5,Python,IT Services,Lateral
102: Wipro,2021,Project Manager,9,26.0,Java,IT Services,Lateral
103: Accenture,2021,Analyst,2,9.0,SQL,Consulting,Lateral
104: Zoho,2021,QA Engineer,3,10.5,Selenium,Product,Lateral
105: TCS,2021,Business Analyst,5,14.5,SQL,IT Services,Lateral
106: HCL,2021,DevOps Engineer,4,15.0,Docker,IT Services,Lateral
107: Infosys,2021,Junior Developer,1,5.5,C++,IT Services,Campus
108: Wipro,2021,Data Analyst,3,12.0,Python,IT Services,Lateral
109: Accenture,2021,Technology Consultant,6,22.0,Java,Consulting,Lateral
110: Zoho,2021,Product Manager,8,27.0,Agile,Product,Lateral
111: TCS,2021,Software Engineer,2,9.0,JavaScript,IT Services,Campus
112: HCL,2021,QA Engineer,2,8.5,Selenium,IT Services,Campus
113: Infosys,2021,Cloud Engineer,5,18.0,AWS,IT Services,Lateral
114: Wipro,2021,Junior Analyst,1,5.2,SQL,IT Services,Campus
115: Accenture,2021,Senior Analyst,4,15.0,Python,Consulting,Lateral
116: Zoho,2021,ML Engineer,4,24.0,TensorFlow,Product,Lateral
117: TCS,2021,Data Scientist,5,21.0,Python,IT Services,Lateral
118: HCL,2021,Cloud Architect,7,28.0,AWS,IT Services,Lateral
119: Infosys,2021,Senior Developer,5,17.0,Java,IT Services,Lateral
120: Wipro,2021,Network Engineer,3,10.5,Cisco,IT Services,Lateral
121: Accenture,2021,Manager,9,38.0,Agile,Consulting,Lateral
122: Zoho,2021,Frontend Developer,3,13.0,React,Product,Lateral
123: TCS,2021,Security Analyst,4,15.0,Cybersecurity,IT Services,Lateral
124: HCL,2021,SAP Consultant,6,21.0,SAP,IT Services,Lateral
125: Infosys,2021,Scrum Master,5,18.0,Agile,IT Services,Lateral
126: Wipro,2021,Full Stack Developer,3,14.0,Node.js,IT Services,Lateral
127: Accenture,2021,Data Engineer,4,18.0,Spark,Consulting,Lateral
128: Zoho,2021,Android Developer,3,14.0,Kotlin,Product,Lateral
129: TCS,2021,iOS Developer,4,16.5,Swift,IT Services,Lateral
130: HCL,2021,BI Developer,5,17.0,Tableau,IT Services,Lateral
131: Infosys,2021,ETL Developer,4,14.0,Informatica,IT Services,Lateral
132: Wipro,2021,RPA Developer,3,13.0,UiPath,IT Services,Lateral
133: Accenture,2021,AI Engineer,5,28.0,Python,Consulting,Lateral
134: Zoho,2022,Software Engineer,2,10.5,Java,Product,Campus
135: TCS,2022,Systems Analyst,5,12.5,Python,IT Services,Lateral
136: HCL,2022,Junior Developer,1,6.5,C++,IT Services,Campus
137: Infosys,2022,Technology Analyst,3,12.5,Java,IT Services,Lateral
138: Wipro,2022,Software Engineer,2,8.5,JavaScript,IT Services,Campus
139: Accenture,2022,Associate,1,8.0,SQL,Consulting,Campus
140: Zoho,2022,Senior Developer,6,23.0,Python,Product,Lateral
141: TCS,2022,Project Lead,8,24.0,Java,IT Services,Lateral
142: HCL,2022,Software Engineer,2,9.5,JavaScript,IT Services,Campus
143: Infosys,2022,Senior Systems Engineer,4,15.5,Python,IT Services,Lateral
144: Wipro,2022,Project Manager,9,29.0,Java,IT Services,Lateral
145: Accenture,2022,Analyst,2,10.5,SQL,Consulting,Lateral
146: Zoho,2022,QA Engineer,3,12.0,Selenium,Product,Lateral
147: TCS,2022,Business Analyst,5,16.5,SQL,IT Services,Lateral
148: HCL,2022,DevOps Engineer,4,17.5,Docker,IT Services,Lateral
149: Infosys,2022,Junior Developer,1,6.5,C++,IT Services,Campus
150: Wipro,2022,Data Analyst,3,14.0,Python,IT Services,Lateral
151: Accenture,2022,Technology Consultant,6,25.0,Java,Consulting,Lateral
152: Zoho,2022,Product Manager,8,32.0,Agile,Product,Lateral
153: TCS,2022,Software Engineer,2,10.5,JavaScript,IT Services,Campus
154: HCL,2022,QA Engineer,2,10.0,Selenium,IT Services,Campus
155: Infosys,2022,Cloud Engineer,5,22.0,AWS,IT Services,Lateral
156: Wipro,2022,Junior Analyst,1,6.0,SQL,IT Services,Campus
157: Accenture,2022,Senior Analyst,4,17.5,Python,Consulting,Lateral
158: Zoho,2022,ML Engineer,4,28.0,TensorFlow,Product,Lateral
159: TCS,2022,Data Scientist,5,25.0,Python,IT Services,Lateral
160: HCL,2022,Cloud Architect,7,32.0,AWS,IT Services,Lateral
161: Infosys,2022,Senior Developer,5,20.0,Java,IT Services,Lateral
162: Wipro,2022,Network Engineer,3,12.0,Cisco,IT Services,Lateral
163: Accenture,2022,Manager,9,44.0,Agile,Consulting,Lateral
164: Zoho,2022,Frontend Developer,3,16.0,React,Product,Lateral
165: TCS,2022,Security Analyst,4,18.0,Cybersecurity,IT Services,Lateral
166: HCL,2022,SAP Consultant,6,24.0,SAP,IT Services,Lateral
167: Infosys,2022,Scrum Master,5,20.0,Agile,IT Services,Lateral
168: Wipro,2022,Full Stack Developer,3,16.0,Node.js,IT Services,Lateral
169: Accenture,2022,Data Engineer,4,22.0,Spark,Consulting,Lateral
170: Zoho,2022,Android Developer,3,17.0,Kotlin,Product,Lateral
171: TCS,2022,iOS Developer,4,19.0,Swift,IT Services,Lateral
172: HCL,2022,BI Developer,5,20.0,Tableau,IT Services,Lateral
173: Infosys,2022,ETL Developer,4,16.5,Informatica,IT Services,Lateral
174: Wipro,2022,RPA Developer,3,15.0,UiPath,IT Services,Lateral
175: Accenture,2022,AI Engineer,5,34.0,Python,Consulting,Lateral
176: Zoho,2022,Backend Developer,4,18.0,Go,Product,Lateral
177: TCS,2022,Platform Engineer,5,22.0,Kubernetes,IT Services,Lateral
178: HCL,2022,Site Reliability Engineer,6,27.0,Linux,IT Services,Lateral
179: Infosys,2022,Blockchain Developer,4,24.0,Solidity,IT Services,Lateral
180: Wipro,2022,Solution Architect,8,35.0,AWS,IT Services,Lateral
181: Accenture,2022,UX Designer,3,15.0,Figma,Consulting,Lateral
182: Zoho,2023,Software Engineer,2,12.0,Java,Product,Campus
183: TCS,2023,Systems Analyst,5,13.5,Python,IT Services,Lateral
184: HCL,2023,Junior Developer,1,7.5,C++,IT Services,Campus
185: Infosys,2023,Technology Analyst,3,14.0,Java,IT Services,Lateral
186: Wipro,2023,Software Engineer,2,9.5,JavaScript,IT Services,Campus
187: Accenture,2023,Associate,1,9.0,SQL,Consulting,Campus
188: Zoho,2023,Senior Developer,6,26.0,Python,Product,Lateral
189: TCS,2023,Project Lead,8,27.0,Java,IT Services,Lateral
190: HCL,2023,Software Engineer,2,10.5,JavaScript,IT Services,Campus
191: Infosys,2023,Senior Systems Engineer,4,17.5,Python,IT Services,Lateral
192: Wipro,2023,Project Manager,9,32.0,Java,IT Services,Lateral
193: Accenture,2023,Analyst,2,12.0,SQL,Consulting,Lateral
194: Zoho,2023,QA Engineer,3,13.5,Selenium,Product,Lateral
195: TCS,2023,Business Analyst,5,18.0,SQL,IT Services,Lateral
196: HCL,2023,DevOps Engineer,4,20.0,Docker,IT Services,Lateral
197: Infosys,2023,Junior Developer,1,7.0,C++,IT Services,Campus
198: Wipro,2023,Data Analyst,3,15.5,Python,IT Services,Lateral
199: Accenture,2023,Technology Consultant,6,28.0,Java,Consulting,Lateral
200: Zoho,2023,Product Manager,8,36.0,Agile,Product,Lateral
201: TCS,2023,Software Engineer,2,12.0,JavaScript,IT Services,Campus
202: HCL,2023,QA Engineer,2,11.5,Selenium,IT Services,Campus
203: Infosys,2023,Cloud Engineer,5,25.0,AWS,IT Services,Lateral
204: Wipro,2023,Junior Analyst,1,6.8,SQL,IT Services,Campus
205: Accenture,2023,Senior Analyst,4,20.0,Python,Consulting,Lateral
206: Zoho,2023,ML Engineer,4,32.0,TensorFlow,Product,Lateral
207: TCS,2023,Data Scientist,5,28.0,Python,IT Services,Lateral
208: HCL,2023,Cloud Architect,7,36.0,AWS,IT Services,Lateral
209: Infosys,2023,Senior Developer,5,22.0,Java,IT Services,Lateral
210: Wipro,2023,Network Engineer,3,13.5,Cisco,IT Services,Lateral
211: Accenture,2023,Manager,9,50.0,Agile,Consulting,Lateral
212: Zoho,2023,Frontend Developer,3,18.0,React,Product,Lateral
213: TCS,2023,Security Analyst,4,21.0,Cybersecurity,IT Services,Lateral
214: HCL,2023,SAP Consultant,6,27.0,SAP,IT Services,Lateral
215: Infosys,2023,Scrum Master,5,22.0,Agile,IT Services,Lateral
216: Wipro,2023,Full Stack Developer,3,18.0,Node.js,IT Services,Lateral
217: Accenture,2023,Data Engineer,4,26.0,Spark,Consulting,Lateral
218: Zoho,2023,Android Developer,3,20.0,Kotlin,Product,Lateral
219: TCS,2023,iOS Developer,4,22.0,Swift,IT Services,Lateral
220: HCL,2023,BI Developer,5,23.0,Tableau,IT Services,Lateral
221: Infosys,2023,ETL Developer,4,18.0,Informatica,IT Services,Lateral
222: Wipro,2023,RPA Developer,3,17.0,UiPath,IT Services,Lateral
223: Accenture,2023,AI Engineer,5,40.0,Python,Consulting,Lateral
224: Zoho,2023,Backend Developer,4,22.0,Go,Product,Lateral
225: TCS,2023,Platform Engineer,5,26.0,Kubernetes,IT Services,Lateral
226: HCL,2023,Site Reliability Engineer,6,31.0,Linux,IT Services,Lateral
227: Infosys,2023,Blockchain Developer,4,27.0,Solidity,IT Services,Lateral
228: Wipro,2023,Solution Architect,8,40.0,AWS,IT Services,Lateral
229: Accenture,2023,UX Designer,3,18.0,Figma,Consulting,Lateral
230: Zoho,2023,GenAI Engineer,3,28.0,LLM,Product,Lateral
231: TCS,2023,Prompt Engineer,2,18.0,LLM,IT Services,Lateral
232: HCL,2023,MLOps Engineer,4,26.0,Python,IT Services,Lateral
233: Infosys,2023,Cybersecurity Analyst,5,24.0,SIEM,IT Services,Lateral
234: Wipro,2023,Cloud Security Engineer,4,23.0,AWS,IT Services,Lateral
235: Accenture,2023,Director,12,75.0,Strategy,Consulting,Lateral
236: Zoho,2024,Software Engineer,2,14.0,Java,Product,Campus
237: TCS,2024,Systems Analyst,5,15.0,Python,IT Services,Lateral
238: HCL,2024,Junior Developer,1,8.5,C++,IT Services,Campus
239: Infosys,2024,Technology Analyst,3,15.5,Java,IT Services,Lateral
240: Wipro,2024,Software Engineer,2,11.0,JavaScript,IT Services,Campus
241: Accenture,2024,Associate,1,10.5,SQL,Consulting,Campus
242: Zoho,2024,Senior Developer,6,30.0,Python,Product,Lateral
243: TCS,2024,Project Lead,8,30.0,Java,IT Services,Lateral
244: HCL,2024,Software Engineer,2,12.0,JavaScript,IT Services,Campus
245: Infosys,2024,Senior Systems Engineer,4,19.5,Python,IT Services,Lateral
246: Wipro,2024,Project Manager,9,35.0,Java,IT Services,Lateral
247: Accenture,2024,Analyst,2,13.5,SQL,Consulting,Lateral
248: Zoho,2024,QA Engineer,3,15.0,Selenium,Product,Lateral
249: TCS,2024,Business Analyst,5,20.0,SQL,IT Services,Lateral
250: HCL,2024,DevOps Engineer,4,22.0,Docker,IT Services,Lateral
251: Infosys,2024,Junior Developer,1,8.0,C++,IT Services,Campus
252: Wipro,2024,Data Analyst,3,17.0,Python,IT Services,Lateral
253: Accenture,2024,Technology Consultant,6,31.0,Java,Consulting,Lateral
254: Zoho,2024,Product Manager,8,42.0,Agile,Product,Lateral
255: TCS,2024,Software Engineer,2,13.5,JavaScript,IT Services,Campus
256: HCL,2024,QA Engineer,2,13.0,Selenium,IT Services,Campus
257: Infosys,2024,Cloud Engineer,5,28.0,AWS,IT Services,Lateral
258: Wipro,2024,Junior Analyst,1,7.5,SQL,IT Services,Campus
259: Accenture,2024,Senior Analyst,4,22.0,Python,Consulting,Lateral
260: Zoho,2024,ML Engineer,4,38.0,TensorFlow,Product,Lateral
261: TCS,2024,Data Scientist,5,32.0,Python,IT Services,Lateral
262: HCL,2024,Cloud Architect,7,40.0,AWS,IT Services,Lateral
263: Infosys,2024,Senior Developer,5,25.0,Java,IT Services,Lateral
264: Wipro,2024,Network Engineer,3,15.0,Cisco,IT Services,Lateral
265: Accenture,2024,Manager,9,56.0,Agile,Consulting,Lateral
266: Zoho,2024,Frontend Developer,3,21.0,React,Product,Lateral
267: TCS,2024,Security Analyst,4,24.0,Cybersecurity,IT Services,Lateral
268: HCL,2024,SAP Consultant,6,30.0,SAP,IT Services,Lateral
269: Infosys,2024,Scrum Master,5,25.0,Agile,IT Services,Lateral
270: Wipro,2024,Full Stack Developer,3,21.0,Node.js,IT Services,Lateral
271: Accenture,2024,Data Engineer,4,30.0,Spark,Consulting,Lateral
272: Zoho,2024,Android Developer,3,23.0,Kotlin,Product,Lateral
273: TCS,2024,iOS Developer,4,25.0,Swift,IT Services,Lateral
274: HCL,2024,BI Developer,5,26.0,Tableau,IT Services,Lateral
275: Infosys,2024,ETL Developer,4,20.0,Informatica,IT Services,Lateral
276: Wipro,2024,RPA Developer,3,19.0,UiPath,IT Services,Lateral
277: Accenture,2024,AI Engineer,5,48.0,Python,Consulting,Lateral
278: Zoho,2024,Backend Developer,4,26.0,Go,Product,Lateral
279: TCS,2024,Platform Engineer,5,30.0,Kubernetes,IT Services,Lateral
280: HCL,2024,Site Reliability Engineer,6,35.0,Linux,IT Services,Lateral
281: Infosys,2024,Blockchain Developer,4,30.0,Solidity,IT Services,Lateral
282: Wipro,2024,Solution Architect,8,45.0,AWS,IT Services,Lateral
283: Accenture,2024,UX Designer,3,21.0,Figma,Consulting,Lateral
284: Zoho,2024,GenAI Engineer,3,34.0,LLM,Product,Lateral
285: TCS,2024,Prompt Engineer,2,22.0,LLM,IT Services,Lateral
286: HCL,2024,MLOps Engineer,4,30.0,Python,IT Services,Lateral
287: Infosys,2024,Cybersecurity Analyst,5,27.0,SIEM,IT Services,Lateral
288: Wipro,2024,Cloud Security Engineer,4,26.0,AWS,IT Services,Lateral
289: Accenture,2024,Director,12,85.0,Strategy,Consulting,Lateral
290: Zoho,2024,VP Engineering,14,95.0,Leadership,Product,Lateral
291: TCS,2024,Delivery Manager,11,55.0,Agile,IT Services,Lateral
292: HCL,2024,Principal Architect,10,60.0,AWS,IT Services,Lateral
293: Infosys,2024,Senior Manager,10,58.0,Java,IT Services,Lateral
294: Wipro,2024,Associate VP,12,70.0,Strategy,IT Services,Lateral
295: Zoho,2018,Backend Developer,3,9.0,Go,Product,Lateral
296: TCS,2019,Platform Engineer,4,11.0,Kubernetes,IT Services,Lateral
297: HCL,2020,Site Reliability Engineer,5,16.0,Linux,IT Services,Lateral
298: Infosys,2021,Android Developer,2,12.0,Kotlin,IT Services,Campus
299: Wipro,2022,GenAI Engineer,3,22.0,LLM,IT Services,Lateral
300: Accenture,2023,ML Engineer,6,45.0,TensorFlow,Consulting,Lateral
301: TCS,2024,Cybersecurity Manager,10,52.0,SIEM,IT Services,Lateral
"""

clean = re.sub(r"^\d+:\s", "", raw_data.strip(), flags=re.MULTILINE)

with open("public/company_data.csv", "w") as f:
    f.write(clean)

print("Data recovered successfully.")
