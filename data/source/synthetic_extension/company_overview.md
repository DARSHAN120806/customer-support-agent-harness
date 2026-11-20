# Company Overview: synthetic records

Imported from the extended knowledge base uploaded on 20 November 2026.
These records are NOT searchable by the assistant. scripts/import_synthetic_data.py turns them into data/orders.json and data/internal/.

> Everything below this line is generated test data. It is not real. All files in this pack share the same order IDs, dates and amounts. Data snapshot: **2026-11-20 09:00 ET**. Times are Eastern Time. Amounts are USD.

## Data conventions

- Order IDs run JL-10001 to JL-11000 (orders placed 2026-06-01 to 2026-11-20). Orders are identified by order ID plus the email on the order.

- Order status values: processing, dispatched, delivered, cancelled, lost.

- Dispatch happens at 16:00 ET on the dispatch date. Orders placed before 14:00 ET on a business day dispatch that day; otherwise the next business day (Personalised Leather Notebook adds 2 business days).

- US public holidays used for business days: 2026-06-19, 2026-07-03, 2026-09-07, 2026-10-12, 2026-11-11, 2026-11-26, 2026-12-25.

- Related-record IDs: RT = return, RF = refund, WC = warranty claim, INV = carrier investigation, DMG = damaged package report, DS = refund dispute, ADR = address change, TK = support ticket.

## Support team roster

| Agent | Role | Hours (ET) |
|---|---|---|
| Priya N. | Support agent | Mon–Fri 9:00–18:00 |
| Marcus T. | Support agent | Mon–Fri 9:00–18:00 |
| Elena R. | Support agent | Mon–Fri 9:00–18:00 |
| Dan K. | Support agent | Mon–Fri 9:00–18:00 |
| Sofia L. | Support agent | Mon–Fri 9:00–18:00 |
| Helen W. (Senior) | Senior reviewer (refund disputes) | Mon–Fri 9:00–18:00 |

## Stock snapshot

| Product | SKU | Units in stock | Status | Back-in-stock sign-ups |
|---|---|---|---|---|
| Bluetooth Speaker Mini | SKU-EL-101 | 98 | In stock | — |
| Wireless Earbuds Pro | SKU-EL-102 | 118 | In stock | — |
| LED Desk Lamp | SKU-EL-103 | 201 | In stock | — |
| Electric Kettle 1.7L | SKU-EL-104 | 165 | In stock | — |
| Smart Plug (2-Pack) | SKU-EL-105 | 150 | In stock | — |
| Oak Side Table | SKU-FU-201 | 60 | In stock | — |
| Wool Throw Blanket | SKU-HW-301 | 0 | Out of stock | 2 |
| Cast Iron Skillet | SKU-HW-302 | 140 | In stock | — |
| Ceramic Pour-Over Coffee Set | SKU-HW-303 | 164 | In stock | — |
| Ceramic Planter Set | SKU-HW-304 | 9 | Low stock | — |
| Bamboo Cutting Board | SKU-HW-305 | 185 | In stock | — |
| Linen Napkins (Set of 4) | SKU-HW-306 | 155 | In stock | — |
| Adjustable Phone Stand | SKU-HW-307 | 196 | In stock | — |
| Scented Soy Candle | SKU-HW-308 | 156 | In stock | — |
| Personalised Leather Notebook | SKU-PE-401 | 41 | In stock | — |

## Sales summary by product (non-cancelled orders)

| Product | Units sold | Revenue |
|---|---|---|
| Bluetooth Speaker Mini | 170 | $6,798.30 |
| Wireless Earbuds Pro | 168 | $13,272.00 |
| LED Desk Lamp | 133 | $4,588.50 |
| Electric Kettle 1.7L | 146 | $6,570.00 |
| Smart Plug (2-Pack) | 124 | $3,100.00 |
| Oak Side Table | 49 | $6,321.00 |
| Wool Throw Blanket | 91 | $6,188.00 |
| Cast Iron Skillet | 105 | $5,775.00 |
| Ceramic Pour-Over Coffee Set | 84 | $3,528.00 |
| Ceramic Planter Set | 100 | $3,200.00 |
| Bamboo Cutting Board | 136 | $3,264.00 |
| Linen Napkins (Set of 4) | 112 | $2,072.00 |
| Adjustable Phone Stand | 95 | $1,425.00 |
| Scented Soy Candle | 173 | $2,076.00 |
| Personalised Leather Notebook | 77 | $2,233.00 |
| Juniper Lane Gift Card | 66 | $4,100.00 |

## Monthly summary

| Month | Orders placed | Cancelled | Revenue (non-cancelled) |
|---|---|---|---|
| 2026-06 | 177 | 9 | $14,880.83 |
| 2026-07 | 181 | 12 | $14,202.81 |
| 2026-08 | 183 | 9 | $14,632.89 |
| 2026-09 | 184 | 6 | $14,137.41 |
| 2026-10 | 184 | 12 | $13,486.74 |
| 2026-11 | 91 | 7 | $6,822.51 |

## Customer directory

| Email | Name | City | State | Account created | Newsletter | Orders |
|---|---|---|---|---|---|---|
| aaliyah.alvarez34@mailbox.example | Aaliyah Alvarez | Richmond | VA | 2021-09-22 | No | 2 |
| aaliyah.alvarez@mailbox.example | Aaliyah Alvarez | Orlando | FL | 2024-11-04 | No | 1 |
| aaliyah.anderson@mailbox.example | Aaliyah Anderson | Tampa | FL | 2022-09-08 | Yes | 1 |
| aaliyah.brooks@inbox.example | Aaliyah Brooks | San Francisco | CA | 2022-07-03 | No | 1 |
| aaliyah.carter@inbox.example | Aaliyah Carter | Minneapolis | MN | 2026-04-11 | No | 1 |
| aaliyah.chen85@inbox.example | Aaliyah Chen | New York | NY | 2021-08-23 | No | 1 |
| aaliyah.daniels17@webmail.example | Aaliyah Daniels | Baltimore | MD | 2021-07-22 | Yes | 2 |
| aaliyah.edwards@inbox.example | Aaliyah Edwards | Indianapolis | IN | 2025-03-17 | Yes | 1 |
| aaliyah.gray72@webmail.example | Aaliyah Gray | Des Moines | IA | 2021-09-23 | Yes | 2 |
| aaliyah.gupta31@webmail.example | Aaliyah Gupta | Louisville | KY | 2024-03-01 | Yes | 1 |
| aaliyah.kim@mailbox.example | Aaliyah Kim | Buffalo | NY | 2025-02-07 | No | 1 |
| aaliyah.ortiz@webmail.example | Aaliyah Ortiz | Los Angeles | CA | 2023-04-02 | No | 5 |
| aaliyah.sanders@webmail.example | Aaliyah Sanders | Kansas City | MO | 2022-06-21 | Yes | 1 |
| aaliyah.singh@webmail.example | Aaliyah Singh | Portland | ME | 2024-01-13 | Yes | 2 |
| abigail.bishop@mailbox.example | Abigail Bishop | New Orleans | LA | 2024-08-10 | Yes | 3 |
| abigail.brooks@webmail.example | Abigail Brooks | Portland | ME | 2022-08-30 | No | 1 |
| abigail.daniels36@inbox.example | Abigail Daniels | Honolulu | HI | 2026-08-09 | No | 1 |
| abigail.davis66@inbox.example | Abigail Davis | Des Moines | IA | 2021-08-10 | Yes | 2 |
| abigail.ellis51@webmail.example | Abigail Ellis | Richmond | VA | 2024-07-16 | No | 1 |
| abigail.flores@webmail.example | Abigail Flores | Columbus | OH | 2026-01-31 | No | 1 |
| abigail.garcia76@inbox.example | Abigail Garcia | Baltimore | MD | 2022-02-16 | Yes | 1 |
| abigail.harris63@inbox.example | Abigail Harris | Portland | ME | 2025-01-22 | Yes | 1 |
| abigail.hughes@mailbox.example | Abigail Hughes | Orlando | FL | 2026-02-19 | No | 1 |
| abigail.jackson62@mailbox.example | Abigail Jackson | Atlanta | GA | 2025-01-29 | No | 1 |
| abigail.kowalski72@webmail.example | Abigail Kowalski | Minneapolis | MN | 2022-12-05 | No | 1 |
| abigail.larson@webmail.example | Abigail Larson | Pittsburgh | PA | 2022-02-10 | Yes | 1 |
| abigail.martinez48@webmail.example | Abigail Martinez | Detroit | MI | 2023-08-24 | No | 1 |
| abigail.martinez@mailbox.example | Abigail Martinez | Portland | ME | 2023-12-02 | No | 1 |
| abigail.morgan86@webmail.example | Abigail Morgan | Los Angeles | CA | 2023-06-24 | No | 1 |
| abigail.thompson55@webmail.example | Abigail Thompson | Los Angeles | CA | 2023-08-10 | No | 2 |
| abigail.underwood51@mailbox.example | Abigail Underwood | Orlando | FL | 2023-12-12 | No | 1 |
| aiden.anderson82@inbox.example | Aiden Anderson | Columbus | OH | 2022-01-05 | Yes | 1 |
| aiden.bishop46@webmail.example | Aiden Bishop | Houston | TX | 2023-01-02 | No | 1 |
| aiden.carter97@mailbox.example | Aiden Carter | Buffalo | NY | 2024-08-25 | Yes | 1 |
| aiden.gray47@mailbox.example | Aiden Gray | Honolulu | HI | 2023-12-27 | No | 1 |
| aiden.jackson@webmail.example | Aiden Jackson | Houston | TX | 2025-10-24 | Yes | 2 |
| aiden.kelly@webmail.example | Aiden Kelly | San Francisco | CA | 2025-02-11 | Yes | 1 |
| aiden.kim91@inbox.example | Aiden Kim | Milwaukee | WI | 2026-03-27 | No | 1 |
| aiden.lewis@inbox.example | Aiden Lewis | Des Moines | IA | 2026-05-23 | Yes | 1 |
| aiden.lopez@inbox.example | Aiden Lopez | Tampa | FL | 2025-04-01 | Yes | 1 |
| aiden.martinez@inbox.example | Aiden Martinez | Minneapolis | MN | 2026-05-04 | Yes | 1 |
| aiden.novak@inbox.example | Aiden Novak | Indianapolis | IN | 2025-01-03 | No | 1 |
| aiden.ortiz33@inbox.example | Aiden Ortiz | Tampa | FL | 2022-02-10 | No | 1 |
| aiden.owens83@mailbox.example | Aiden Owens | Portland | OR | 2023-02-06 | Yes | 1 |
| aiden.rossi20@inbox.example | Aiden Rossi | Denver | CO | 2022-05-21 | No | 2 |
| aiden.vasquez@mailbox.example | Aiden Vasquez | New Orleans | LA | 2025-06-05 | No | 1 |
| aiden.xu99@inbox.example | Aiden Xu | Dallas | TX | 2022-07-25 | No | 1 |
| amelia.bennett@inbox.example | Amelia Bennett | Washington | DC | 2022-10-06 | Yes | 1 |
| amelia.brooks34@webmail.example | Amelia Brooks | Kansas City | MO | 2022-07-15 | No | 1 |
| amelia.chen40@inbox.example | Amelia Chen | Omaha | NE | 2026-08-23 | Yes | 1 |
| amelia.daniels94@mailbox.example | Amelia Daniels | Detroit | MI | 2023-06-28 | Yes | 2 |
| amelia.edwards@inbox.example | Amelia Edwards | Boise | ID | 2026-07-24 | No | 1 |
| amelia.ellis@inbox.example | Amelia Ellis | Kansas City | MO | 2026-07-10 | Yes | 1 |
| amelia.harris15@mailbox.example | Amelia Harris | Dallas | TX | 2025-12-29 | Yes | 1 |
| amelia.jackson6@webmail.example | Amelia Jackson | Nashville | TN | 2024-07-01 | Yes | 1 |
| amelia.jensen@webmail.example | Amelia Jensen | Raleigh | NC | 2024-01-02 | No | 1 |
| amelia.larson93@webmail.example | Amelia Larson | San Francisco | CA | 2023-04-03 | Yes | 2 |
| amelia.morgan64@inbox.example | Amelia Morgan | Portland | OR | 2026-07-15 | Yes | 1 |
| amelia.sanders@mailbox.example | Amelia Sanders | Dallas | TX | 2022-03-05 | No | 1 |
| amelia.turner64@inbox.example | Amelia Turner | Boston | MA | 2023-06-18 | Yes | 1 |
| amelia.walker@mailbox.example | Amelia Walker | Philadelphia | PA | 2022-06-20 | No | 2 |
| aria.alvarez62@webmail.example | Aria Alvarez | Austin | TX | 2026-06-11 | Yes | 1 |
| aria.anderson@inbox.example | Aria Anderson | New Orleans | LA | 2025-02-15 | No | 1 |
| aria.chen@inbox.example | Aria Chen | New Orleans | LA | 2025-09-11 | Yes | 2 |
| aria.chen@webmail.example | Aria Chen | Portland | ME | 2024-05-11 | Yes | 1 |
| aria.hughes@mailbox.example | Aria Hughes | Detroit | MI | 2023-05-23 | No | 1 |
| aria.johnson79@inbox.example | Aria Johnson | Seattle | WA | 2024-12-24 | Yes | 1 |
| aria.kelly@webmail.example | Aria Kelly | Pittsburgh | PA | 2026-05-19 | No | 1 |
| aria.kim21@mailbox.example | Aria Kim | Orlando | FL | 2023-01-09 | Yes | 2 |
| aria.kim64@inbox.example | Aria Kim | Buffalo | NY | 2022-06-28 | No | 1 |
| aria.reyes94@webmail.example | Aria Reyes | Raleigh | NC | 2024-05-27 | Yes | 1 |
| aria.singh81@webmail.example | Aria Singh | New York | NY | 2025-07-01 | Yes | 1 |
| aria.young@mailbox.example | Aria Young | Orlando | FL | 2022-10-25 | Yes | 1 |
| arjun.davis@webmail.example | Arjun Davis | Milwaukee | WI | 2025-03-26 | Yes | 2 |
| arjun.donovan@inbox.example | Arjun Donovan | Denver | CO | 2023-04-20 | No | 1 |
| arjun.garcia91@inbox.example | Arjun Garcia | Miami | FL | 2022-01-18 | Yes | 1 |
| arjun.iyer@mailbox.example | Arjun Iyer | Orlando | FL | 2024-03-18 | Yes | 1 |
| arjun.kim63@inbox.example | Arjun Kim | Detroit | MI | 2024-01-14 | Yes | 1 |
| arjun.martinez@inbox.example | Arjun Martinez | Milwaukee | WI | 2026-02-10 | No | 2 |
| arjun.morgan96@mailbox.example | Arjun Morgan | Baltimore | MD | 2023-01-12 | Yes | 1 |
| arjun.okafor@mailbox.example | Arjun Okafor | Los Angeles | CA | 2025-08-10 | No | 2 |
| arjun.owens58@webmail.example | Arjun Owens | Raleigh | NC | 2022-11-18 | No | 1 |
| arjun.petrov@inbox.example | Arjun Petrov | Portland | ME | 2022-12-17 | No | 2 |
| arjun.petrov@webmail.example | Arjun Petrov | San Diego | CA | 2025-06-01 | Yes | 1 |
| arjun.rossi@inbox.example | Arjun Rossi | Honolulu | HI | 2023-07-28 | No | 1 |
| arjun.xu@webmail.example | Arjun Xu | Orlando | FL | 2025-02-08 | Yes | 1 |
| arjun.zimmerman79@webmail.example | Arjun Zimmerman | Phoenix | AZ | 2022-11-08 | No | 1 |
| ava.alvarez@inbox.example | Ava Alvarez | Nashville | TN | 2026-05-28 | No | 1 |
| ava.campbell@webmail.example | Ava Campbell | Burlington | VT | 2023-09-14 | No | 2 |
| ava.davis@mailbox.example | Ava Davis | San Francisco | CA | 2022-09-21 | Yes | 2 |
| ava.ellis@mailbox.example | Ava Ellis | Portland | OR | 2021-12-14 | No | 1 |
| ava.gray@webmail.example | Ava Gray | Seattle | WA | 2022-03-16 | No | 1 |
| ava.hammond@mailbox.example | Ava Hammond | Portland | OR | 2023-09-14 | No | 2 |
| ava.ingram41@inbox.example | Ava Ingram | Charlotte | NC | 2025-06-25 | No | 1 |
| ava.jensen@webmail.example | Ava Jensen | Detroit | MI | 2026-06-06 | No | 1 |
| ava.martinez@inbox.example | Ava Martinez | Nashville | TN | 2024-10-29 | Yes | 1 |
| ava.martinez@mailbox.example | Ava Martinez | Baltimore | MD | 2026-05-08 | Yes | 1 |
| ava.morgan@mailbox.example | Ava Morgan | Oklahoma City | OK | 2024-08-04 | No | 1 |
| ava.thompson46@mailbox.example | Ava Thompson | Honolulu | HI | 2025-09-11 | Yes | 1 |
| ava.turner67@webmail.example | Ava Turner | Salt Lake City | UT | 2024-02-25 | Yes | 3 |
| ava.vasquez@mailbox.example | Ava Vasquez | Los Angeles | CA | 2024-11-11 | No | 1 |
| brandon.bishop@mailbox.example | Brandon Bishop | Salt Lake City | UT | 2025-10-13 | No | 1 |
| brandon.edwards@mailbox.example | Brandon Edwards | Philadelphia | PA | 2023-01-03 | Yes | 1 |
| brandon.hammond23@mailbox.example | Brandon Hammond | Austin | TX | 2026-05-14 | Yes | 4 |
| brandon.harris20@mailbox.example | Brandon Harris | Charlotte | NC | 2024-06-14 | No | 2 |
| brandon.jackson85@webmail.example | Brandon Jackson | San Francisco | CA | 2024-05-23 | Yes | 1 |
| brandon.kim15@webmail.example | Brandon Kim | Albuquerque | NM | 2021-08-22 | Yes | 1 |
| brandon.patel14@webmail.example | Brandon Patel | Anchorage | AK | 2025-03-25 | Yes | 1 |
| brandon.perry@inbox.example | Brandon Perry | Charlotte | NC | 2025-10-28 | No | 1 |
| brandon.reyes75@inbox.example | Brandon Reyes | Minneapolis | MN | 2022-08-06 | No | 1 |
| brandon.walsh@webmail.example | Brandon Walsh | New York | NY | 2025-02-18 | No | 1 |
| brandon.yamamoto26@mailbox.example | Brandon Yamamoto | San Diego | CA | 2025-08-11 | No | 1 |
| caleb.chen15@webmail.example | Caleb Chen | Minneapolis | MN | 2022-03-28 | No | 1 |
| caleb.edwards@webmail.example | Caleb Edwards | Miami | FL | 2024-04-14 | No | 2 |
| caleb.gray@webmail.example | Caleb Gray | Des Moines | IA | 2024-10-08 | No | 1 |
| caleb.hammond80@webmail.example | Caleb Hammond | Las Vegas | NV | 2025-05-15 | Yes | 4 |
| caleb.harris86@webmail.example | Caleb Harris | Burlington | VT | 2025-11-13 | No | 1 |
| caleb.iyer69@mailbox.example | Caleb Iyer | Denver | CO | 2025-07-07 | No | 1 |
| caleb.iyer@inbox.example | Caleb Iyer | Charlotte | NC | 2025-07-24 | No | 1 |
| caleb.jensen37@inbox.example | Caleb Jensen | Los Angeles | CA | 2022-10-03 | No | 1 |
| caleb.kowalski@mailbox.example | Caleb Kowalski | Denver | CO | 2022-09-13 | No | 1 |
| caleb.lewis7@inbox.example | Caleb Lewis | Dallas | TX | 2023-01-29 | No | 1 |
| caleb.lewis@webmail.example | Caleb Lewis | Providence | RI | 2024-01-02 | No | 1 |
| caleb.nguyen@mailbox.example | Caleb Nguyen | Milwaukee | WI | 2023-05-24 | Yes | 1 |
| caleb.ortiz@inbox.example | Caleb Ortiz | Indianapolis | IN | 2025-12-04 | Yes | 2 |
| caleb.patel@inbox.example | Caleb Patel | Charlotte | NC | 2025-12-28 | Yes | 1 |
| caleb.vasquez17@webmail.example | Caleb Vasquez | Richmond | VA | 2024-04-16 | Yes | 1 |
| chloe.anderson30@mailbox.example | Chloe Anderson | Buffalo | NY | 2025-06-20 | Yes | 1 |
| chloe.bishop@webmail.example | Chloe Bishop | Charlotte | NC | 2023-07-09 | Yes | 1 |
| chloe.chen@inbox.example | Chloe Chen | New Orleans | LA | 2025-10-13 | No | 1 |
| chloe.davis@inbox.example | Chloe Davis | Charlotte | NC | 2026-03-04 | No | 1 |
| chloe.ellis@inbox.example | Chloe Ellis | Cleveland | OH | 2026-01-15 | No | 1 |
| chloe.foster42@mailbox.example | Chloe Foster | Seattle | WA | 2022-07-15 | No | 1 |
| chloe.foster7@mailbox.example | Chloe Foster | Providence | RI | 2026-04-10 | No | 1 |
| chloe.gupta75@mailbox.example | Chloe Gupta | Raleigh | NC | 2023-01-04 | No | 2 |
| chloe.okafor@inbox.example | Chloe Okafor | Charlotte | NC | 2022-01-12 | Yes | 2 |
| chloe.perry@webmail.example | Chloe Perry | Houston | TX | 2022-03-07 | No | 1 |
| chloe.quinn77@webmail.example | Chloe Quinn | Portland | ME | 2024-10-30 | No | 2 |
| chloe.reyes@webmail.example | Chloe Reyes | Des Moines | IA | 2026-10-13 | No | 1 |
| chloe.sanders88@webmail.example | Chloe Sanders | Des Moines | IA | 2022-03-30 | Yes | 1 |
| chloe.underwood11@mailbox.example | Chloe Underwood | San Francisco | CA | 2025-01-05 | No | 1 |
| chloe.walsh21@mailbox.example | Chloe Walsh | Detroit | MI | 2024-03-31 | No | 2 |
| chloe.zimmerman@mailbox.example | Chloe Zimmerman | Baltimore | MD | 2021-10-13 | Yes | 1 |
| devon.alvarez@webmail.example | Devon Alvarez | Miami | FL | 2026-09-11 | Yes | 1 |
| devon.bishop77@webmail.example | Devon Bishop | Kansas City | MO | 2024-03-05 | Yes | 1 |
| devon.fischer79@webmail.example | Devon Fischer | Washington | DC | 2021-07-30 | Yes | 2 |
| devon.gray17@inbox.example | Devon Gray | Pittsburgh | PA | 2025-06-20 | Yes | 1 |
| devon.ingram74@webmail.example | Devon Ingram | Phoenix | AZ | 2024-07-05 | Yes | 1 |
| devon.ingram@mailbox.example | Devon Ingram | Washington | DC | 2025-04-28 | No | 1 |
| devon.johnson87@mailbox.example | Devon Johnson | Charlotte | NC | 2022-01-04 | Yes | 2 |
| devon.lewis@webmail.example | Devon Lewis | Austin | TX | 2022-07-24 | No | 1 |
| devon.martinez@webmail.example | Devon Martinez | Salt Lake City | UT | 2025-10-02 | No | 1 |
| devon.thompson36@webmail.example | Devon Thompson | Dallas | TX | 2022-07-12 | Yes | 1 |
| devon.underwood99@webmail.example | Devon Underwood | Providence | RI | 2023-04-21 | No | 1 |
| diego.daniels49@mailbox.example | Diego Daniels | Indianapolis | IN | 2023-12-01 | No | 2 |
| diego.edwards14@inbox.example | Diego Edwards | Oklahoma City | OK | 2024-12-01 | Yes | 1 |
| diego.ellis@inbox.example | Diego Ellis | Minneapolis | MN | 2026-07-31 | No | 1 |
| diego.fischer29@webmail.example | Diego Fischer | Cleveland | OH | 2026-03-11 | No | 1 |
| diego.garcia@inbox.example | Diego Garcia | Houston | TX | 2024-12-22 | Yes | 2 |
| diego.gray@webmail.example | Diego Gray | Columbus | OH | 2025-12-09 | No | 1 |
| diego.gupta@mailbox.example | Diego Gupta | Portland | ME | 2025-10-11 | No | 1 |
| diego.hughes@webmail.example | Diego Hughes | Cleveland | OH | 2025-10-23 | No | 1 |
| diego.jackson8@webmail.example | Diego Jackson | Portland | OR | 2026-01-26 | No | 1 |
| diego.kowalski42@webmail.example | Diego Kowalski | Pittsburgh | PA | 2023-11-27 | No | 1 |
| diego.lopez@mailbox.example | Diego Lopez | Atlanta | GA | 2021-12-26 | No | 1 |
| diego.sanders64@mailbox.example | Diego Sanders | Orlando | FL | 2022-07-04 | Yes | 3 |
| diego.singh@inbox.example | Diego Singh | Boston | MA | 2025-09-05 | Yes | 1 |
| diego.thompson@mailbox.example | Diego Thompson | San Francisco | CA | 2023-06-19 | No | 1 |
| diego.turner@mailbox.example | Diego Turner | Cleveland | OH | 2025-06-02 | Yes | 1 |
| dylan.campbell@webmail.example | Dylan Campbell | Boston | MA | 2026-05-31 | Yes | 1 |
| dylan.chen@mailbox.example | Dylan Chen | Dallas | TX | 2024-04-07 | Yes | 1 |
| dylan.daniels43@inbox.example | Dylan Daniels | Oklahoma City | OK | 2025-06-19 | No | 1 |
| dylan.davis@mailbox.example | Dylan Davis | Kansas City | MO | 2024-01-10 | No | 1 |
| dylan.edwards1@mailbox.example | Dylan Edwards | Louisville | KY | 2023-09-15 | No | 1 |
| dylan.foster@mailbox.example | Dylan Foster | Baltimore | MD | 2024-10-04 | Yes | 2 |
| dylan.garcia@webmail.example | Dylan Garcia | Philadelphia | PA | 2023-02-13 | Yes | 1 |
| dylan.nguyen55@inbox.example | Dylan Nguyen | Austin | TX | 2026-04-20 | No | 1 |
| dylan.reyes91@inbox.example | Dylan Reyes | Oklahoma City | OK | 2022-02-11 | No | 1 |
| dylan.rossi45@webmail.example | Dylan Rossi | Orlando | FL | 2022-10-04 | No | 1 |
| dylan.rossi@mailbox.example | Dylan Rossi | Cleveland | OH | 2025-12-17 | Yes | 1 |
| elijah.carter@mailbox.example | Elijah Carter | Richmond | VA | 2024-09-21 | No | 1 |
| elijah.daniels@inbox.example | Elijah Daniels | Buffalo | NY | 2026-01-27 | No | 3 |
| elijah.foster@webmail.example | Elijah Foster | Seattle | WA | 2022-08-04 | No | 1 |
| elijah.gupta@webmail.example | Elijah Gupta | Denver | CO | 2026-05-01 | No | 3 |
| elijah.ingram@webmail.example | Elijah Ingram | Cleveland | OH | 2023-07-15 | No | 1 |
| elijah.jackson12@webmail.example | Elijah Jackson | New York | NY | 2021-11-16 | No | 1 |
| elijah.jensen13@mailbox.example | Elijah Jensen | Baltimore | MD | 2022-07-24 | No | 1 |
| elijah.jensen@mailbox.example | Elijah Jensen | Tampa | FL | 2024-07-01 | No | 1 |
| elijah.kim78@webmail.example | Elijah Kim | Tampa | FL | 2026-01-04 | Yes | 1 |
| elijah.kowalski8@mailbox.example | Elijah Kowalski | Austin | TX | 2024-07-31 | No | 1 |
| elijah.quinn43@mailbox.example | Elijah Quinn | Minneapolis | MN | 2022-05-29 | No | 1 |
| elijah.walker@mailbox.example | Elijah Walker | Indianapolis | IN | 2025-03-28 | Yes | 1 |
| elijah.walsh@inbox.example | Elijah Walsh | Boise | ID | 2021-12-23 | Yes | 1 |
| ella.donovan60@mailbox.example | Ella Donovan | Nashville | TN | 2024-03-25 | No | 1 |
| ella.harris17@webmail.example | Ella Harris | Kansas City | MO | 2023-10-11 | No | 1 |
| ella.harris81@webmail.example | Ella Harris | San Francisco | CA | 2023-05-31 | Yes | 2 |
| ella.lopez55@mailbox.example | Ella Lopez | Phoenix | AZ | 2022-05-20 | No | 1 |
| ella.perry@webmail.example | Ella Perry | Houston | TX | 2024-09-03 | No | 1 |
| ella.sanders65@webmail.example | Ella Sanders | Milwaukee | WI | 2022-09-06 | No | 1 |
| ella.thompson@mailbox.example | Ella Thompson | Omaha | NE | 2023-05-29 | No | 1 |
| ella.vasquez@webmail.example | Ella Vasquez | Raleigh | NC | 2022-05-11 | Yes | 1 |
| ella.xu38@mailbox.example | Ella Xu | New Orleans | LA | 2024-07-10 | No | 1 |
| ella.zimmerman@webmail.example | Ella Zimmerman | Detroit | MI | 2023-12-10 | Yes | 1 |
| emma.campbell8@inbox.example | Emma Campbell | Charlotte | NC | 2026-09-24 | No | 1 |
| emma.daniels@inbox.example | Emma Daniels | New York | NY | 2024-08-24 | No | 2 |
| emma.edwards38@webmail.example | Emma Edwards | Cleveland | OH | 2024-06-30 | No | 1 |
| emma.flores@mailbox.example | Emma Flores | Milwaukee | WI | 2024-03-03 | Yes | 2 |
| emma.hughes42@webmail.example | Emma Hughes | Indianapolis | IN | 2026-03-05 | No | 1 |
| emma.ingram97@mailbox.example | Emma Ingram | Charlotte | NC | 2023-12-11 | No | 2 |
| emma.mitchell@mailbox.example | Emma Mitchell | Austin | TX | 2025-01-29 | Yes | 1 |
| emma.ramirez@mailbox.example | Emma Ramirez | Salt Lake City | UT | 2026-06-13 | Yes | 1 |
| emma.reyes97@mailbox.example | Emma Reyes | Detroit | MI | 2022-11-25 | No | 2 |
| ethan.anderson44@inbox.example | Ethan Anderson | Los Angeles | CA | 2024-01-22 | No | 2 |
| ethan.anderson@mailbox.example | Ethan Anderson | Las Vegas | NV | 2022-06-25 | No | 2 |
| ethan.brooks@webmail.example | Ethan Brooks | Denver | CO | 2025-12-02 | No | 1 |
| ethan.daniels@inbox.example | Ethan Daniels | Providence | RI | 2022-12-12 | Yes | 1 |
| ethan.davis4@inbox.example | Ethan Davis | Miami | FL | 2025-06-09 | Yes | 1 |
| ethan.ellis3@mailbox.example | Ethan Ellis | Oklahoma City | OK | 2024-01-24 | Yes | 1 |
| ethan.flores40@inbox.example | Ethan Flores | Salt Lake City | UT | 2023-02-04 | Yes | 1 |
| ethan.foster66@mailbox.example | Ethan Foster | Los Angeles | CA | 2022-06-10 | Yes | 1 |
| ethan.gray82@inbox.example | Ethan Gray | Charlotte | NC | 2026-04-11 | No | 1 |
| ethan.hammond26@mailbox.example | Ethan Hammond | Miami | FL | 2022-02-18 | Yes | 1 |
| ethan.kelly@inbox.example | Ethan Kelly | Los Angeles | CA | 2024-01-19 | No | 1 |
| ethan.kim19@inbox.example | Ethan Kim | Indianapolis | IN | 2025-09-14 | Yes | 1 |
| ethan.lopez97@mailbox.example | Ethan Lopez | Oklahoma City | OK | 2022-12-11 | No | 1 |
| ethan.martinez40@webmail.example | Ethan Martinez | Des Moines | IA | 2023-09-21 | Yes | 1 |
| ethan.reyes@inbox.example | Ethan Reyes | Seattle | WA | 2022-03-17 | No | 1 |
| ethan.thompson@mailbox.example | Ethan Thompson | Anchorage | AK | 2026-01-28 | Yes | 1 |
| ethan.turner96@mailbox.example | Ethan Turner | Louisville | KY | 2025-09-26 | No | 3 |
| evelyn.bennett52@mailbox.example | Evelyn Bennett | Richmond | VA | 2023-11-04 | Yes | 1 |
| evelyn.brooks@inbox.example | Evelyn Brooks | Indianapolis | IN | 2022-03-31 | Yes | 1 |
| evelyn.campbell77@mailbox.example | Evelyn Campbell | Honolulu | HI | 2025-07-17 | No | 1 |
| evelyn.daniels53@inbox.example | Evelyn Daniels | New Orleans | LA | 2022-07-11 | No | 1 |
| evelyn.ellis@webmail.example | Evelyn Ellis | Philadelphia | PA | 2025-07-10 | Yes | 1 |
| evelyn.gray92@mailbox.example | Evelyn Gray | Charlotte | NC | 2025-10-01 | Yes | 2 |
| evelyn.gray@mailbox.example | Evelyn Gray | Denver | CO | 2022-01-07 | Yes | 1 |
| evelyn.gupta@mailbox.example | Evelyn Gupta | New Orleans | LA | 2025-03-15 | No | 1 |
| evelyn.hughes@mailbox.example | Evelyn Hughes | Raleigh | NC | 2026-04-06 | Yes | 1 |
| evelyn.ingram37@mailbox.example | Evelyn Ingram | Portland | ME | 2023-06-06 | No | 6 |
| evelyn.johnson33@inbox.example | Evelyn Johnson | Detroit | MI | 2022-03-28 | Yes | 1 |
| evelyn.johnson37@webmail.example | Evelyn Johnson | Providence | RI | 2022-05-22 | No | 1 |
| evelyn.kowalski63@mailbox.example | Evelyn Kowalski | Phoenix | AZ | 2026-08-26 | No | 1 |
| evelyn.okafor78@mailbox.example | Evelyn Okafor | Houston | TX | 2024-07-16 | No | 1 |
| evelyn.okafor@inbox.example | Evelyn Okafor | Des Moines | IA | 2022-07-05 | Yes | 1 |
| evelyn.ortiz15@webmail.example | Evelyn Ortiz | Buffalo | NY | 2022-02-09 | No | 1 |
| evelyn.sanders96@mailbox.example | Evelyn Sanders | Portland | OR | 2022-09-06 | No | 3 |
| evelyn.yamamoto63@webmail.example | Evelyn Yamamoto | Burlington | VT | 2022-02-17 | No | 1 |
| fatima.alvarez@mailbox.example | Fatima Alvarez | Albuquerque | NM | 2025-11-22 | No | 1 |
| fatima.anderson26@mailbox.example | Fatima Anderson | Los Angeles | CA | 2025-10-15 | No | 1 |
| fatima.anderson@mailbox.example | Fatima Anderson | Baltimore | MD | 2025-06-12 | No | 1 |
| fatima.bennett@webmail.example | Fatima Bennett | New York | NY | 2025-10-23 | No | 1 |
| fatima.bishop46@inbox.example | Fatima Bishop | Phoenix | AZ | 2025-01-13 | Yes | 1 |
| fatima.campbell66@webmail.example | Fatima Campbell | Columbus | OH | 2022-02-20 | Yes | 1 |
| fatima.donovan88@mailbox.example | Fatima Donovan | New York | NY | 2022-02-24 | No | 1 |
| fatima.ellis93@mailbox.example | Fatima Ellis | Providence | RI | 2022-01-24 | Yes | 1 |
| fatima.fischer69@mailbox.example | Fatima Fischer | Detroit | MI | 2026-08-02 | No | 1 |
| fatima.foster63@webmail.example | Fatima Foster | Indianapolis | IN | 2026-03-27 | No | 1 |
| gabriel.alvarez@mailbox.example | Gabriel Alvarez | Orlando | FL | 2023-10-28 | No | 2 |
| gabriel.anderson@mailbox.example | Gabriel Anderson | Oklahoma City | OK | 2026-02-01 | No | 1 |
| gabriel.chen44@webmail.example | Gabriel Chen | Los Angeles | CA | 2024-09-29 | No | 1 |
| gabriel.davis67@inbox.example | Gabriel Davis | Portland | ME | 2025-02-18 | No | 1 |
| gabriel.foster60@inbox.example | Gabriel Foster | Des Moines | IA | 2021-10-16 | Yes | 2 |
| gabriel.garcia1@mailbox.example | Gabriel Garcia | Denver | CO | 2025-04-13 | Yes | 1 |
| gabriel.hughes@webmail.example | Gabriel Hughes | Philadelphia | PA | 2023-01-29 | No | 1 |
| gabriel.jensen@mailbox.example | Gabriel Jensen | Philadelphia | PA | 2024-05-13 | No | 1 |
| gabriel.johnson@mailbox.example | Gabriel Johnson | Denver | CO | 2022-12-06 | Yes | 1 |
| gabriel.morgan19@inbox.example | Gabriel Morgan | Providence | RI | 2022-08-05 | Yes | 1 |
| gabriel.nguyen@mailbox.example | Gabriel Nguyen | Raleigh | NC | 2025-09-05 | No | 1 |
| gabriel.owens63@inbox.example | Gabriel Owens | Anchorage | AK | 2023-11-18 | No | 1 |
| gabriel.rossi52@inbox.example | Gabriel Rossi | Seattle | WA | 2023-01-27 | No | 1 |
| gabriel.vasquez@webmail.example | Gabriel Vasquez | Detroit | MI | 2025-10-10 | Yes | 3 |
| gabriel.walsh31@inbox.example | Gabriel Walsh | New York | NY | 2022-04-29 | Yes | 2 |
| gabriel.zimmerman69@inbox.example | Gabriel Zimmerman | Louisville | KY | 2026-01-17 | No | 1 |
| grace.bennett@inbox.example | Grace Bennett | Los Angeles | CA | 2026-03-17 | No | 1 |
| grace.daniels26@mailbox.example | Grace Daniels | Chicago | IL | 2023-01-14 | Yes | 1 |
| grace.ellis@webmail.example | Grace Ellis | Miami | FL | 2024-05-23 | No | 1 |
| grace.gray9@inbox.example | Grace Gray | Baltimore | MD | 2022-06-07 | No | 2 |
| grace.novak@inbox.example | Grace Novak | Denver | CO | 2025-01-06 | No | 1 |
| grace.patel@inbox.example | Grace Patel | Houston | TX | 2024-01-19 | Yes | 1 |
| grace.quinn@mailbox.example | Grace Quinn | Nashville | TN | 2022-02-18 | No | 1 |
| grace.sanders47@webmail.example | Grace Sanders | Des Moines | IA | 2023-03-06 | Yes | 1 |
| grace.sanders@webmail.example | Grace Sanders | Richmond | VA | 2021-12-30 | Yes | 1 |
| grace.walker28@inbox.example | Grace Walker | Las Vegas | NV | 2024-08-27 | No | 1 |
| grace.walker@mailbox.example | Grace Walker | Burlington | VT | 2026-06-20 | No | 1 |
| grace.walsh@webmail.example | Grace Walsh | Raleigh | NC | 2023-02-08 | No | 1 |
| grace.yamamoto20@inbox.example | Grace Yamamoto | Boise | ID | 2022-06-03 | No | 1 |
| grace.young75@inbox.example | Grace Young | Burlington | VT | 2026-02-28 | Yes | 1 |
| harper.kelly28@inbox.example | Harper Kelly | Salt Lake City | UT | 2025-04-07 | No | 1 |
| harper.larson18@inbox.example | Harper Larson | Kansas City | MO | 2024-05-24 | Yes | 1 |
| harper.morgan30@webmail.example | Harper Morgan | Chicago | IL | 2022-12-01 | Yes | 2 |
| harper.morgan82@webmail.example | Harper Morgan | Des Moines | IA | 2026-01-25 | No | 2 |
| harper.okafor37@webmail.example | Harper Okafor | Salt Lake City | UT | 2023-02-24 | No | 1 |
| harper.reyes17@inbox.example | Harper Reyes | Orlando | FL | 2022-07-12 | No | 3 |
| harper.underwood@mailbox.example | Harper Underwood | Denver | CO | 2023-10-27 | No | 1 |
| harper.vasquez20@mailbox.example | Harper Vasquez | Louisville | KY | 2022-09-22 | No | 2 |
| harper.walker@webmail.example | Harper Walker | Phoenix | AZ | 2023-05-17 | No | 1 |
| harper.walsh@webmail.example | Harper Walsh | Columbus | OH | 2025-02-23 | Yes | 1 |
| hazel.anderson55@inbox.example | Hazel Anderson | Washington | DC | 2025-11-25 | No | 1 |
| hazel.ellis52@inbox.example | Hazel Ellis | Baltimore | MD | 2025-09-10 | Yes | 1 |
| hazel.flores37@inbox.example | Hazel Flores | Houston | TX | 2026-02-18 | No | 1 |
| hazel.hughes26@mailbox.example | Hazel Hughes | Miami | FL | 2023-08-13 | Yes | 4 |
| hazel.jackson8@webmail.example | Hazel Jackson | Providence | RI | 2022-05-18 | Yes | 2 |
| hazel.quinn29@inbox.example | Hazel Quinn | Omaha | NE | 2023-12-30 | Yes | 2 |
| henry.anderson@inbox.example | Henry Anderson | Chicago | IL | 2024-12-15 | Yes | 1 |
| henry.bennett@inbox.example | Henry Bennett | Raleigh | NC | 2022-06-17 | No | 1 |
| henry.daniels40@inbox.example | Henry Daniels | Los Angeles | CA | 2025-01-08 | No | 2 |
| henry.donovan33@mailbox.example | Henry Donovan | Columbus | OH | 2025-08-10 | No | 1 |
| henry.edwards29@inbox.example | Henry Edwards | Chicago | IL | 2024-10-26 | No | 2 |
| henry.edwards95@webmail.example | Henry Edwards | Tampa | FL | 2026-04-18 | Yes | 1 |
| henry.hammond95@inbox.example | Henry Hammond | Denver | CO | 2024-08-21 | Yes | 1 |
| henry.harris@mailbox.example | Henry Harris | Nashville | TN | 2024-12-23 | Yes | 1 |
| henry.hughes66@webmail.example | Henry Hughes | Orlando | FL | 2023-11-30 | No | 1 |
| henry.lewis@mailbox.example | Henry Lewis | Salt Lake City | UT | 2023-08-25 | No | 1 |
| henry.singh32@inbox.example | Henry Singh | New Orleans | LA | 2023-12-05 | No | 1 |
| henry.vasquez@webmail.example | Henry Vasquez | Honolulu | HI | 2022-12-02 | Yes | 2 |
| henry.yamamoto33@mailbox.example | Henry Yamamoto | San Diego | CA | 2025-11-10 | No | 1 |
| henry.yamamoto72@inbox.example | Henry Yamamoto | Nashville | TN | 2022-04-29 | No | 1 |
| henry.young@webmail.example | Henry Young | Orlando | FL | 2022-09-01 | Yes | 2 |
| hiro.brooks62@mailbox.example | Hiro Brooks | Austin | TX | 2024-11-02 | Yes | 1 |
| hiro.chen72@webmail.example | Hiro Chen | Los Angeles | CA | 2024-02-21 | Yes | 1 |
| hiro.chen@inbox.example | Hiro Chen | Detroit | MI | 2023-02-17 | No | 2 |
| hiro.davis60@inbox.example | Hiro Davis | Boston | MA | 2026-05-07 | No | 1 |
| hiro.ellis@inbox.example | Hiro Ellis | San Francisco | CA | 2023-10-13 | No | 1 |
| hiro.ellis@mailbox.example | Hiro Ellis | Boston | MA | 2022-10-23 | No | 1 |
| hiro.harris27@webmail.example | Hiro Harris | Des Moines | IA | 2022-06-19 | Yes | 1 |
| hiro.harris50@mailbox.example | Hiro Harris | Tampa | FL | 2023-12-12 | Yes | 1 |
| hiro.johnson@webmail.example | Hiro Johnson | Washington | DC | 2026-04-04 | No | 1 |
| hiro.mitchell@webmail.example | Hiro Mitchell | Anchorage | AK | 2025-09-14 | Yes | 1 |
| hiro.ramirez27@inbox.example | Hiro Ramirez | Las Vegas | NV | 2026-01-18 | Yes | 1 |
| hiro.ramirez@webmail.example | Hiro Ramirez | Austin | TX | 2024-01-18 | No | 1 |
| hiro.rossi38@webmail.example | Hiro Rossi | Miami | FL | 2024-03-24 | Yes | 1 |
| hiro.walker@webmail.example | Hiro Walker | Columbus | OH | 2026-08-09 | No | 1 |
| ingrid.alvarez@mailbox.example | Ingrid Alvarez | Baltimore | MD | 2022-08-23 | Yes | 1 |
| ingrid.anderson40@mailbox.example | Ingrid Anderson | Boise | ID | 2023-09-27 | No | 1 |
| ingrid.anderson@webmail.example | Ingrid Anderson | Anchorage | AK | 2024-12-23 | Yes | 1 |
| ingrid.gray@mailbox.example | Ingrid Gray | Portland | ME | 2023-04-16 | Yes | 2 |
| ingrid.kim57@inbox.example | Ingrid Kim | Anchorage | AK | 2024-06-20 | No | 2 |
| ingrid.nelson@mailbox.example | Ingrid Nelson | New York | NY | 2021-08-31 | No | 2 |
| ingrid.owens@inbox.example | Ingrid Owens | Albuquerque | NM | 2024-01-08 | Yes | 1 |
| ingrid.quinn79@webmail.example | Ingrid Quinn | Detroit | MI | 2022-03-18 | No | 1 |
| ingrid.singh@mailbox.example | Ingrid Singh | Houston | TX | 2022-03-07 | Yes | 1 |
| ingrid.turner74@inbox.example | Ingrid Turner | Indianapolis | IN | 2024-12-13 | No | 1 |
| ingrid.turner@inbox.example | Ingrid Turner | Raleigh | NC | 2024-02-17 | No | 1 |
| ingrid.walsh@inbox.example | Ingrid Walsh | Buffalo | NY | 2024-08-10 | Yes | 1 |
| isaac.garcia72@inbox.example | Isaac Garcia | Richmond | VA | 2026-02-09 | Yes | 4 |
| isaac.harris@mailbox.example | Isaac Harris | Indianapolis | IN | 2022-05-01 | No | 1 |
| isaac.hughes@mailbox.example | Isaac Hughes | Orlando | FL | 2026-06-11 | No | 1 |
| isaac.kelly7@webmail.example | Isaac Kelly | New York | NY | 2021-12-13 | No | 1 |
| isaac.kim46@webmail.example | Isaac Kim | Minneapolis | MN | 2024-10-26 | No | 1 |
| isaac.martinez95@webmail.example | Isaac Martinez | Philadelphia | PA | 2022-03-30 | Yes | 1 |
| isaac.owens@webmail.example | Isaac Owens | Las Vegas | NV | 2022-04-21 | No | 1 |
| isaac.petrov88@mailbox.example | Isaac Petrov | Seattle | WA | 2024-12-27 | Yes | 2 |
| isaac.petrov@mailbox.example | Isaac Petrov | Los Angeles | CA | 2023-09-22 | Yes | 3 |
| isaac.reyes50@inbox.example | Isaac Reyes | Austin | TX | 2024-11-26 | Yes | 1 |
| isaac.reyes@inbox.example | Isaac Reyes | Salt Lake City | UT | 2023-05-23 | Yes | 1 |
| isaac.vasquez@mailbox.example | Isaac Vasquez | San Diego | CA | 2024-07-12 | Yes | 1 |
| isabella.campbell77@mailbox.example | Isabella Campbell | San Francisco | CA | 2023-09-02 | No | 1 |
| isabella.foster13@inbox.example | Isabella Foster | Houston | TX | 2023-03-07 | No | 2 |
| isabella.johnson@mailbox.example | Isabella Johnson | Las Vegas | NV | 2021-10-09 | No | 1 |
| isabella.perry77@webmail.example | Isabella Perry | Albuquerque | NM | 2026-04-16 | No | 1 |
| isabella.ramirez84@inbox.example | Isabella Ramirez | Los Angeles | CA | 2025-07-30 | Yes | 1 |
| isabella.vasquez43@mailbox.example | Isabella Vasquez | Seattle | WA | 2024-02-15 | No | 1 |
| jackson.anderson55@webmail.example | Jackson Anderson | Denver | CO | 2026-06-16 | No | 1 |
| jackson.daniels74@mailbox.example | Jackson Daniels | Miami | FL | 2024-08-23 | Yes | 1 |
| jackson.donovan@mailbox.example | Jackson Donovan | Milwaukee | WI | 2022-03-01 | Yes | 2 |
| jackson.hughes28@inbox.example | Jackson Hughes | Anchorage | AK | 2026-01-09 | No | 1 |
| jackson.kim@webmail.example | Jackson Kim | Charlotte | NC | 2024-08-23 | Yes | 1 |
| jackson.larson68@webmail.example | Jackson Larson | Nashville | TN | 2026-09-02 | No | 2 |
| jackson.martinez78@mailbox.example | Jackson Martinez | Minneapolis | MN | 2023-01-28 | No | 1 |
| jackson.nelson@webmail.example | Jackson Nelson | Phoenix | AZ | 2024-03-16 | No | 2 |
| jackson.ortiz31@webmail.example | Jackson Ortiz | Houston | TX | 2026-09-04 | No | 1 |
| jackson.patel@mailbox.example | Jackson Patel | Cleveland | OH | 2024-01-27 | Yes | 1 |
| jackson.quinn@inbox.example | Jackson Quinn | San Francisco | CA | 2022-05-06 | No | 3 |
| jamal.daniels54@inbox.example | Jamal Daniels | Seattle | WA | 2024-01-07 | No | 1 |
| jamal.donovan5@mailbox.example | Jamal Donovan | Cleveland | OH | 2023-01-25 | Yes | 2 |
| jamal.garcia@webmail.example | Jamal Garcia | Oklahoma City | OK | 2022-10-22 | Yes | 1 |
| jamal.gray42@inbox.example | Jamal Gray | Dallas | TX | 2022-07-28 | No | 1 |
| jamal.harris49@webmail.example | Jamal Harris | Orlando | FL | 2023-09-27 | Yes | 1 |
| jamal.harris@inbox.example | Jamal Harris | Louisville | KY | 2024-12-02 | No | 3 |
| jamal.kim50@mailbox.example | Jamal Kim | Portland | OR | 2022-07-22 | Yes | 2 |
| jamal.lewis@inbox.example | Jamal Lewis | Atlanta | GA | 2022-12-24 | No | 1 |
| jamal.lopez@mailbox.example | Jamal Lopez | Des Moines | IA | 2021-11-25 | Yes | 1 |
| jamal.nguyen@inbox.example | Jamal Nguyen | Anchorage | AK | 2026-10-26 | No | 1 |
| jamal.novak@webmail.example | Jamal Novak | Louisville | KY | 2023-01-14 | No | 1 |
| jamal.reyes55@inbox.example | Jamal Reyes | Cleveland | OH | 2024-09-11 | Yes | 1 |
| jamal.thompson70@mailbox.example | Jamal Thompson | Indianapolis | IN | 2022-02-08 | Yes | 1 |
| jamal.walsh96@inbox.example | Jamal Walsh | Charlotte | NC | 2025-07-07 | Yes | 1 |
| jamal.young@mailbox.example | Jamal Young | Burlington | VT | 2024-04-10 | No | 1 |
| jamal.zimmerman@inbox.example | Jamal Zimmerman | Philadelphia | PA | 2025-09-10 | No | 1 |
| james.alvarez34@mailbox.example | James Alvarez | Seattle | WA | 2023-04-30 | No | 1 |
| james.chen59@webmail.example | James Chen | Detroit | MI | 2021-12-24 | Yes | 1 |
| james.fischer@webmail.example | James Fischer | Nashville | TN | 2025-03-22 | No | 1 |
| james.flores35@webmail.example | James Flores | Columbus | OH | 2024-11-24 | Yes | 1 |
| james.foster@mailbox.example | James Foster | Washington | DC | 2026-08-25 | No | 1 |
| james.gray@inbox.example | James Gray | Baltimore | MD | 2025-11-17 | Yes | 1 |
| james.hammond93@webmail.example | James Hammond | Las Vegas | NV | 2025-01-14 | Yes | 1 |
| james.johnson73@mailbox.example | James Johnson | Honolulu | HI | 2024-10-30 | Yes | 1 |
| james.larson@mailbox.example | James Larson | Chicago | IL | 2024-12-25 | Yes | 1 |
| james.lopez@mailbox.example | James Lopez | Portland | ME | 2022-04-30 | No | 1 |
| james.morgan@webmail.example | James Morgan | New York | NY | 2021-12-06 | No | 1 |
| james.owens@inbox.example | James Owens | Washington | DC | 2022-02-13 | No | 2 |
| james.petrov@inbox.example | James Petrov | New Orleans | LA | 2025-07-18 | No | 1 |
| james.thompson@mailbox.example | James Thompson | Milwaukee | WI | 2026-05-28 | Yes | 1 |
| james.turner58@mailbox.example | James Turner | Baltimore | MD | 2023-11-09 | Yes | 1 |
| james.underwood@inbox.example | James Underwood | Omaha | NE | 2025-11-02 | Yes | 1 |
| james.xu@webmail.example | James Xu | Pittsburgh | PA | 2026-06-28 | No | 1 |
| julian.alvarez60@mailbox.example | Julian Alvarez | Omaha | NE | 2023-10-27 | Yes | 1 |
| julian.daniels@mailbox.example | Julian Daniels | Boise | ID | 2024-06-27 | Yes | 1 |
| julian.johnson44@webmail.example | Julian Johnson | Nashville | TN | 2024-11-04 | No | 2 |
| julian.kim48@inbox.example | Julian Kim | Kansas City | MO | 2024-01-28 | No | 1 |
| julian.nguyen13@mailbox.example | Julian Nguyen | Washington | DC | 2024-08-02 | Yes | 1 |
| julian.owens85@inbox.example | Julian Owens | Des Moines | IA | 2022-08-02 | Yes | 2 |
| julian.owens9@mailbox.example | Julian Owens | Chicago | IL | 2025-07-24 | Yes | 1 |
| julian.petrov@mailbox.example | Julian Petrov | Austin | TX | 2023-09-29 | No | 1 |
| julian.ramirez7@webmail.example | Julian Ramirez | Baltimore | MD | 2021-08-13 | No | 1 |
| julian.singh@webmail.example | Julian Singh | Washington | DC | 2025-08-28 | Yes | 1 |
| julian.underwood@webmail.example | Julian Underwood | Honolulu | HI | 2025-06-21 | Yes | 1 |
| keisha.bennett@webmail.example | Keisha Bennett | Tampa | FL | 2022-09-24 | No | 1 |
| keisha.ellis46@mailbox.example | Keisha Ellis | Portland | OR | 2023-11-12 | No | 1 |
| keisha.ellis@mailbox.example | Keisha Ellis | Burlington | VT | 2023-02-21 | No | 1 |
| keisha.foster@mailbox.example | Keisha Foster | Baltimore | MD | 2022-03-05 | Yes | 2 |
| keisha.gray@webmail.example | Keisha Gray | Portland | ME | 2023-07-21 | No | 1 |
| keisha.hammond77@inbox.example | Keisha Hammond | New York | NY | 2025-02-27 | No | 1 |
| keisha.ingram64@inbox.example | Keisha Ingram | New York | NY | 2021-10-23 | No | 3 |
| keisha.jensen@inbox.example | Keisha Jensen | Richmond | VA | 2026-08-21 | No | 1 |
| keisha.martinez9@mailbox.example | Keisha Martinez | Las Vegas | NV | 2024-04-04 | Yes | 2 |
| keisha.martinez@webmail.example | Keisha Martinez | Providence | RI | 2022-07-20 | No | 1 |
| keisha.morgan39@webmail.example | Keisha Morgan | Salt Lake City | UT | 2023-08-12 | Yes | 1 |
| keisha.rossi@webmail.example | Keisha Rossi | Oklahoma City | OK | 2022-05-20 | No | 1 |
| keisha.singh6@mailbox.example | Keisha Singh | Chicago | IL | 2026-04-13 | Yes | 1 |
| levi.chen@inbox.example | Levi Chen | Salt Lake City | UT | 2024-09-21 | No | 2 |
| levi.davis@webmail.example | Levi Davis | Seattle | WA | 2023-07-31 | No | 1 |
| levi.edwards27@webmail.example | Levi Edwards | Buffalo | NY | 2023-11-07 | No | 1 |
| levi.gupta61@webmail.example | Levi Gupta | Baltimore | MD | 2023-03-24 | Yes | 1 |
| levi.hughes37@mailbox.example | Levi Hughes | Providence | RI | 2026-02-27 | Yes | 1 |
| levi.jensen@webmail.example | Levi Jensen | Tampa | FL | 2022-08-27 | No | 1 |
| levi.sanders95@mailbox.example | Levi Sanders | Austin | TX | 2022-01-27 | No | 1 |
| levi.singh4@inbox.example | Levi Singh | Houston | TX | 2021-12-20 | Yes | 1 |
| levi.singh53@mailbox.example | Levi Singh | Raleigh | NC | 2024-06-11 | Yes | 2 |
| levi.underwood39@mailbox.example | Levi Underwood | Salt Lake City | UT | 2024-03-17 | No | 2 |
| levi.xu99@mailbox.example | Levi Xu | Los Angeles | CA | 2026-05-12 | No | 1 |
| liam.bennett@webmail.example | Liam Bennett | Oklahoma City | OK | 2023-01-03 | Yes | 4 |
| liam.brooks94@mailbox.example | Liam Brooks | Burlington | VT | 2022-01-28 | Yes | 1 |
| liam.brooks@mailbox.example | Liam Brooks | Raleigh | NC | 2022-07-02 | Yes | 3 |
| liam.campbell@webmail.example | Liam Campbell | Charlotte | NC | 2023-08-29 | No | 1 |
| liam.davis@mailbox.example | Liam Davis | Las Vegas | NV | 2026-05-04 | No | 1 |
| liam.gray89@webmail.example | Liam Gray | Seattle | WA | 2021-12-31 | Yes | 1 |
| liam.gupta53@webmail.example | Liam Gupta | Austin | TX | 2025-02-18 | No | 1 |
| liam.gupta55@webmail.example | Liam Gupta | Las Vegas | NV | 2023-05-04 | No | 1 |
| liam.jensen@webmail.example | Liam Jensen | Seattle | WA | 2022-12-12 | Yes | 1 |
| liam.kim@webmail.example | Liam Kim | Philadelphia | PA | 2024-08-10 | No | 1 |
| liam.martinez64@mailbox.example | Liam Martinez | Milwaukee | WI | 2023-02-07 | Yes | 1 |
| liam.nelson11@webmail.example | Liam Nelson | Las Vegas | NV | 2024-03-01 | Yes | 3 |
| liam.ortiz@inbox.example | Liam Ortiz | Philadelphia | PA | 2024-01-08 | Yes | 1 |
| liam.rossi@mailbox.example | Liam Rossi | Detroit | MI | 2026-01-20 | No | 1 |
| liam.underwood@mailbox.example | Liam Underwood | San Francisco | CA | 2024-05-17 | No | 1 |
| lily.brooks68@inbox.example | Lily Brooks | Milwaukee | WI | 2022-09-27 | Yes | 1 |
| lily.daniels@mailbox.example | Lily Daniels | Richmond | VA | 2025-07-14 | No | 1 |
| lily.davis54@webmail.example | Lily Davis | Las Vegas | NV | 2023-09-24 | No | 1 |
| lily.donovan58@inbox.example | Lily Donovan | Atlanta | GA | 2024-02-09 | No | 1 |
| lily.fischer@webmail.example | Lily Fischer | Chicago | IL | 2024-08-01 | Yes | 2 |
| lily.ingram@inbox.example | Lily Ingram | Oklahoma City | OK | 2025-07-15 | Yes | 1 |
| lily.jackson48@mailbox.example | Lily Jackson | Atlanta | GA | 2025-03-20 | Yes | 2 |
| lily.johnson@mailbox.example | Lily Johnson | Burlington | VT | 2024-11-29 | No | 1 |
| lily.petrov@webmail.example | Lily Petrov | San Diego | CA | 2024-05-20 | Yes | 1 |
| lily.reyes25@mailbox.example | Lily Reyes | Cleveland | OH | 2024-01-29 | No | 1 |
| lily.thompson30@mailbox.example | Lily Thompson | New York | NY | 2024-02-11 | No | 2 |
| lily.turner@webmail.example | Lily Turner | Boston | MA | 2024-07-04 | No | 1 |
| lily.underwood@inbox.example | Lily Underwood | Baltimore | MD | 2024-11-05 | No | 1 |
| lily.vasquez@mailbox.example | Lily Vasquez | Cleveland | OH | 2022-04-19 | No | 1 |
| lily.zimmerman50@webmail.example | Lily Zimmerman | Orlando | FL | 2023-05-16 | No | 3 |
| logan.bennett18@inbox.example | Logan Bennett | New York | NY | 2021-12-06 | Yes | 1 |
| logan.bishop3@inbox.example | Logan Bishop | Providence | RI | 2025-07-07 | No | 1 |
| logan.donovan@inbox.example | Logan Donovan | Charlotte | NC | 2025-11-18 | Yes | 1 |
| logan.garcia@inbox.example | Logan Garcia | New Orleans | LA | 2026-05-27 | No | 1 |
| logan.jensen@mailbox.example | Logan Jensen | Seattle | WA | 2025-08-25 | No | 1 |
| logan.martinez87@inbox.example | Logan Martinez | Chicago | IL | 2024-04-05 | No | 1 |
| logan.ramirez@mailbox.example | Logan Ramirez | Anchorage | AK | 2025-06-20 | Yes | 1 |
| logan.sanders@webmail.example | Logan Sanders | Atlanta | GA | 2021-12-18 | Yes | 2 |
| logan.singh@inbox.example | Logan Singh | Portland | ME | 2025-08-11 | No | 1 |
| logan.thompson@inbox.example | Logan Thompson | Richmond | VA | 2022-08-18 | No | 2 |
| logan.turner@webmail.example | Logan Turner | Atlanta | GA | 2022-05-26 | No | 2 |
| lucas.daniels3@webmail.example | Lucas Daniels | Boise | ID | 2022-06-15 | No | 1 |
| lucas.davis59@inbox.example | Lucas Davis | Oklahoma City | OK | 2024-07-10 | Yes | 1 |
| lucas.kelly51@inbox.example | Lucas Kelly | Des Moines | IA | 2025-12-30 | No | 2 |
| lucas.kim@webmail.example | Lucas Kim | Dallas | TX | 2026-02-23 | No | 1 |
| lucas.lewis90@inbox.example | Lucas Lewis | Las Vegas | NV | 2025-06-29 | No | 1 |
| lucas.nguyen@webmail.example | Lucas Nguyen | Buffalo | NY | 2026-02-06 | Yes | 1 |
| lucas.owens@webmail.example | Lucas Owens | Washington | DC | 2024-10-28 | Yes | 1 |
| lucas.quinn@mailbox.example | Lucas Quinn | Baltimore | MD | 2024-12-18 | No | 4 |
| lucas.quinn@webmail.example | Lucas Quinn | Raleigh | NC | 2026-10-06 | No | 1 |
| lucas.xu84@webmail.example | Lucas Xu | New Orleans | LA | 2024-09-13 | Yes | 1 |
| lucas.young69@webmail.example | Lucas Young | Baltimore | MD | 2023-09-09 | No | 2 |
| lucas.zimmerman70@inbox.example | Lucas Zimmerman | Denver | CO | 2024-05-04 | No | 1 |
| lucia.campbell@mailbox.example | Lucia Campbell | New York | NY | 2022-10-29 | Yes | 1 |
| lucia.ingram@webmail.example | Lucia Ingram | New Orleans | LA | 2025-01-29 | Yes | 1 |
| lucia.larson@webmail.example | Lucia Larson | Washington | DC | 2022-05-25 | Yes | 1 |
| lucia.mitchell6@webmail.example | Lucia Mitchell | Baltimore | MD | 2024-12-18 | Yes | 3 |
| lucia.nguyen@mailbox.example | Lucia Nguyen | Charlotte | NC | 2025-08-22 | Yes | 2 |
| lucia.novak@webmail.example | Lucia Novak | Indianapolis | IN | 2022-05-27 | Yes | 1 |
| lucia.okafor@mailbox.example | Lucia Okafor | Kansas City | MO | 2025-07-21 | No | 1 |
| lucia.patel@mailbox.example | Lucia Patel | San Diego | CA | 2024-07-20 | No | 1 |
| lucia.patel@webmail.example | Lucia Patel | Burlington | VT | 2022-05-04 | Yes | 1 |
| lucia.petrov51@mailbox.example | Lucia Petrov | Washington | DC | 2024-01-29 | Yes | 4 |
| lucia.sanders92@webmail.example | Lucia Sanders | Kansas City | MO | 2025-09-08 | No | 1 |
| lucia.yamamoto@webmail.example | Lucia Yamamoto | Chicago | IL | 2026-02-07 | Yes | 1 |
| marcus.fischer26@mailbox.example | Marcus Fischer | Boise | ID | 2023-07-21 | Yes | 1 |
| marcus.foster18@webmail.example | Marcus Foster | Des Moines | IA | 2023-05-13 | Yes | 1 |
| marcus.kim1@mailbox.example | Marcus Kim | Atlanta | GA | 2025-03-06 | No | 1 |
| marcus.kim@webmail.example | Marcus Kim | Des Moines | IA | 2023-01-24 | No | 1 |
| marcus.patel81@webmail.example | Marcus Patel | Burlington | VT | 2023-02-16 | No | 1 |
| marcus.singh@webmail.example | Marcus Singh | Honolulu | HI | 2023-10-27 | No | 1 |
| marcus.yamamoto36@mailbox.example | Marcus Yamamoto | Phoenix | AZ | 2025-01-10 | No | 1 |
| mason.alvarez79@inbox.example | Mason Alvarez | Milwaukee | WI | 2021-07-04 | No | 1 |
| mason.bishop5@webmail.example | Mason Bishop | Milwaukee | WI | 2022-10-04 | Yes | 1 |
| mason.chen@mailbox.example | Mason Chen | Richmond | VA | 2023-04-29 | No | 2 |
| mason.daniels86@webmail.example | Mason Daniels | Portland | OR | 2026-02-06 | No | 1 |
| mason.gupta52@mailbox.example | Mason Gupta | Pittsburgh | PA | 2026-03-15 | Yes | 3 |
| mason.iyer@inbox.example | Mason Iyer | Nashville | TN | 2024-07-01 | No | 2 |
| mason.iyer@webmail.example | Mason Iyer | Phoenix | AZ | 2025-08-02 | Yes | 1 |
| mason.larson24@mailbox.example | Mason Larson | Oklahoma City | OK | 2026-07-17 | Yes | 1 |
| mason.novak49@webmail.example | Mason Novak | Louisville | KY | 2026-01-22 | No | 1 |
| mason.owens@mailbox.example | Mason Owens | Houston | TX | 2023-03-28 | Yes | 1 |
| mason.perry75@webmail.example | Mason Perry | Providence | RI | 2025-01-02 | No | 1 |
| mason.quinn6@mailbox.example | Mason Quinn | Portland | ME | 2025-03-28 | Yes | 1 |
| mason.singh47@mailbox.example | Mason Singh | Charlotte | NC | 2021-08-25 | No | 1 |
| mason.singh95@inbox.example | Mason Singh | Cleveland | OH | 2023-11-29 | Yes | 1 |
| mason.turner9@inbox.example | Mason Turner | Richmond | VA | 2025-01-25 | No | 1 |
| mason.walsh99@webmail.example | Mason Walsh | Minneapolis | MN | 2022-06-10 | No | 1 |
| mateo.anderson@inbox.example | Mateo Anderson | Phoenix | AZ | 2026-06-24 | No | 1 |
| mateo.bishop@inbox.example | Mateo Bishop | Houston | TX | 2025-04-15 | No | 1 |
| mateo.campbell75@mailbox.example | Mateo Campbell | Omaha | NE | 2025-05-13 | No | 1 |
| mateo.donovan@inbox.example | Mateo Donovan | Boise | ID | 2023-11-06 | Yes | 1 |
| mateo.flores44@mailbox.example | Mateo Flores | Cleveland | OH | 2025-01-04 | No | 1 |
| mateo.harris20@inbox.example | Mateo Harris | Los Angeles | CA | 2024-10-11 | Yes | 1 |
| mateo.larson@inbox.example | Mateo Larson | San Diego | CA | 2026-03-06 | No | 1 |
| mateo.owens60@webmail.example | Mateo Owens | Burlington | VT | 2024-03-18 | Yes | 1 |
| mateo.patel@webmail.example | Mateo Patel | Chicago | IL | 2022-11-18 | No | 1 |
| mateo.perry@mailbox.example | Mateo Perry | Milwaukee | WI | 2025-10-26 | No | 3 |
| mateo.petrov36@inbox.example | Mateo Petrov | Richmond | VA | 2022-06-29 | Yes | 1 |
| mateo.petrov@mailbox.example | Mateo Petrov | Cleveland | OH | 2026-03-23 | No | 1 |
| mateo.ramirez90@mailbox.example | Mateo Ramirez | Louisville | KY | 2025-09-21 | No | 1 |
| mateo.singh@inbox.example | Mateo Singh | Austin | TX | 2026-02-14 | No | 3 |
| mateo.vasquez@inbox.example | Mateo Vasquez | Atlanta | GA | 2023-05-22 | Yes | 1 |
| mateo.walker36@mailbox.example | Mateo Walker | Philadelphia | PA | 2024-08-08 | No | 1 |
| mateo.yamamoto@mailbox.example | Mateo Yamamoto | Honolulu | HI | 2023-06-07 | No | 1 |
| mateo.young@webmail.example | Mateo Young | Raleigh | NC | 2025-08-04 | Yes | 2 |
| maya.alvarez96@webmail.example | Maya Alvarez | Richmond | VA | 2025-05-31 | Yes | 1 |
| maya.bennett@mailbox.example | Maya Bennett | Omaha | NE | 2026-06-15 | Yes | 1 |
| maya.campbell@inbox.example | Maya Campbell | Honolulu | HI | 2025-08-23 | Yes | 2 |
| maya.chen@inbox.example | Maya Chen | Louisville | KY | 2024-12-27 | No | 1 |
| maya.davis27@mailbox.example | Maya Davis | Houston | TX | 2021-09-08 | No | 1 |
| maya.davis27@webmail.example | Maya Davis | New Orleans | LA | 2023-05-24 | No | 1 |
| maya.davis74@inbox.example | Maya Davis | Atlanta | GA | 2024-07-26 | Yes | 3 |
| maya.fischer@mailbox.example | Maya Fischer | Nashville | TN | 2022-03-16 | No | 1 |
| maya.gray@webmail.example | Maya Gray | New Orleans | LA | 2023-10-11 | Yes | 1 |
| maya.gupta21@mailbox.example | Maya Gupta | Orlando | FL | 2021-12-18 | No | 1 |
| maya.kelly26@mailbox.example | Maya Kelly | Burlington | VT | 2024-06-09 | No | 1 |
| maya.kim35@mailbox.example | Maya Kim | Minneapolis | MN | 2025-10-02 | No | 1 |
| maya.larson@mailbox.example | Maya Larson | Milwaukee | WI | 2024-06-25 | No | 1 |
| maya.lewis97@mailbox.example | Maya Lewis | Seattle | WA | 2023-05-29 | No | 1 |
| maya.lopez39@inbox.example | Maya Lopez | Honolulu | HI | 2022-09-24 | No | 4 |
| maya.novak@inbox.example | Maya Novak | Philadelphia | PA | 2026-07-15 | Yes | 1 |
| maya.patel@inbox.example | Maya Patel | San Diego | CA | 2025-02-21 | No | 1 |
| maya.ramirez@mailbox.example | Maya Ramirez | Baltimore | MD | 2025-02-19 | Yes | 1 |
| maya.rossi46@inbox.example | Maya Rossi | Des Moines | IA | 2022-08-12 | No | 1 |
| maya.walker@webmail.example | Maya Walker | Honolulu | HI | 2024-01-18 | Yes | 2 |
| mei.anderson@mailbox.example | Mei Anderson | Des Moines | IA | 2022-08-12 | Yes | 1 |
| mei.daniels@inbox.example | Mei Daniels | Philadelphia | PA | 2023-08-25 | Yes | 2 |
| mei.edwards7@webmail.example | Mei Edwards | Orlando | FL | 2023-01-17 | No | 1 |
| mei.ellis@inbox.example | Mei Ellis | Charlotte | NC | 2026-01-27 | No | 2 |
| mei.gupta58@webmail.example | Mei Gupta | Austin | TX | 2025-01-17 | Yes | 1 |
| mei.kim@webmail.example | Mei Kim | Las Vegas | NV | 2024-03-19 | Yes | 1 |
| mei.larson@mailbox.example | Mei Larson | Boise | ID | 2023-08-27 | No | 2 |
| mei.mitchell55@mailbox.example | Mei Mitchell | Atlanta | GA | 2021-11-23 | No | 1 |
| mei.owens56@mailbox.example | Mei Owens | San Diego | CA | 2023-05-08 | Yes | 2 |
| mei.walker52@webmail.example | Mei Walker | Richmond | VA | 2023-01-21 | No | 2 |
| mei.walsh@webmail.example | Mei Walsh | New York | NY | 2024-08-31 | Yes | 1 |
| mei.yamamoto@webmail.example | Mei Yamamoto | Des Moines | IA | 2026-04-12 | Yes | 1 |
| mei.zimmerman@webmail.example | Mei Zimmerman | Chicago | IL | 2022-10-21 | Yes | 2 |
| mia.alvarez@webmail.example | Mia Alvarez | Phoenix | AZ | 2025-12-11 | No | 1 |
| mia.bennett34@webmail.example | Mia Bennett | Austin | TX | 2023-06-07 | Yes | 2 |
| mia.ellis78@webmail.example | Mia Ellis | Los Angeles | CA | 2024-02-20 | Yes | 1 |
| mia.fischer@inbox.example | Mia Fischer | Nashville | TN | 2021-12-01 | Yes | 1 |
| mia.garcia64@inbox.example | Mia Garcia | Omaha | NE | 2022-07-22 | Yes | 1 |
| mia.gupta@inbox.example | Mia Gupta | New York | NY | 2024-10-26 | No | 2 |
| mia.ingram@mailbox.example | Mia Ingram | Washington | DC | 2023-09-29 | No | 1 |
| mia.iyer25@inbox.example | Mia Iyer | Minneapolis | MN | 2022-02-07 | Yes | 1 |
| mia.jensen@inbox.example | Mia Jensen | Omaha | NE | 2022-09-18 | No | 1 |
| mia.nelson29@webmail.example | Mia Nelson | San Francisco | CA | 2025-08-12 | No | 2 |
| mia.nelson@mailbox.example | Mia Nelson | Baltimore | MD | 2022-07-11 | Yes | 1 |
| mia.nelson@webmail.example | Mia Nelson | Dallas | TX | 2026-03-04 | No | 1 |
| mia.nguyen@mailbox.example | Mia Nguyen | Indianapolis | IN | 2024-06-26 | No | 1 |
| mia.rossi@mailbox.example | Mia Rossi | New York | NY | 2025-10-12 | Yes | 1 |
| mia.singh@inbox.example | Mia Singh | Austin | TX | 2025-09-10 | No | 1 |
| mia.turner52@inbox.example | Mia Turner | Buffalo | NY | 2021-11-27 | Yes | 2 |
| nathan.bennett@inbox.example | Nathan Bennett | Nashville | TN | 2022-11-20 | Yes | 1 |
| nathan.daniels@mailbox.example | Nathan Daniels | Des Moines | IA | 2026-03-09 | Yes | 1 |
| nathan.fischer80@webmail.example | Nathan Fischer | Minneapolis | MN | 2024-11-09 | No | 2 |
| nathan.garcia@mailbox.example | Nathan Garcia | Pittsburgh | PA | 2025-06-03 | Yes | 1 |
| nathan.gray37@mailbox.example | Nathan Gray | Buffalo | NY | 2023-07-30 | No | 1 |
| nathan.kelly24@mailbox.example | Nathan Kelly | Burlington | VT | 2023-01-24 | Yes | 1 |
| nathan.kelly@webmail.example | Nathan Kelly | Dallas | TX | 2021-12-28 | No | 1 |
| nathan.kowalski@inbox.example | Nathan Kowalski | Richmond | VA | 2023-03-14 | No | 1 |
| nathan.perry@inbox.example | Nathan Perry | Richmond | VA | 2022-07-26 | No | 2 |
| nathan.underwood41@inbox.example | Nathan Underwood | Boston | MA | 2024-09-28 | Yes | 1 |
| nathan.yamamoto@mailbox.example | Nathan Yamamoto | Milwaukee | WI | 2022-09-09 | Yes | 3 |
| nathan.young@inbox.example | Nathan Young | Anchorage | AK | 2023-02-02 | Yes | 1 |
| noah.carter12@inbox.example | Noah Carter | Los Angeles | CA | 2023-11-06 | Yes | 1 |
| noah.carter89@mailbox.example | Noah Carter | Milwaukee | WI | 2024-06-17 | No | 1 |
| noah.daniels3@mailbox.example | Noah Daniels | Chicago | IL | 2024-03-17 | Yes | 1 |
| noah.foster48@inbox.example | Noah Foster | Seattle | WA | 2026-07-31 | Yes | 1 |
| noah.ingram@inbox.example | Noah Ingram | Philadelphia | PA | 2023-06-28 | No | 1 |
| noah.jensen@mailbox.example | Noah Jensen | Dallas | TX | 2021-11-27 | Yes | 1 |
| noah.johnson@webmail.example | Noah Johnson | Dallas | TX | 2023-11-21 | No | 1 |
| noah.kelly@webmail.example | Noah Kelly | Cleveland | OH | 2025-01-27 | Yes | 1 |
| noah.kowalski93@webmail.example | Noah Kowalski | Phoenix | AZ | 2024-08-02 | Yes | 1 |
| noah.novak70@mailbox.example | Noah Novak | Boise | ID | 2023-10-12 | No | 2 |
| noah.reyes60@webmail.example | Noah Reyes | Burlington | VT | 2025-09-25 | Yes | 1 |
| noah.turner45@webmail.example | Noah Turner | Buffalo | NY | 2023-05-13 | Yes | 2 |
| noah.young82@webmail.example | Noah Young | Honolulu | HI | 2023-03-08 | Yes | 2 |
| nora.bishop@inbox.example | Nora Bishop | Columbus | OH | 2024-12-26 | No | 1 |
| nora.flores67@webmail.example | Nora Flores | Burlington | VT | 2024-01-30 | No | 1 |
| nora.hughes@inbox.example | Nora Hughes | Minneapolis | MN | 2022-02-19 | Yes | 1 |
| nora.ingram@inbox.example | Nora Ingram | Anchorage | AK | 2025-06-13 | No | 1 |
| nora.larson39@inbox.example | Nora Larson | Tampa | FL | 2022-02-20 | No | 1 |
| nora.martinez97@inbox.example | Nora Martinez | Detroit | MI | 2024-06-19 | Yes | 1 |
| nora.martinez@mailbox.example | Nora Martinez | Kansas City | MO | 2024-11-03 | Yes | 1 |
| nora.novak@inbox.example | Nora Novak | Providence | RI | 2025-09-04 | No | 1 |
| nora.okafor@webmail.example | Nora Okafor | Seattle | WA | 2026-05-20 | Yes | 1 |
| nora.perry47@mailbox.example | Nora Perry | Buffalo | NY | 2021-07-20 | Yes | 2 |
| nora.reyes7@mailbox.example | Nora Reyes | New York | NY | 2025-11-15 | No | 1 |
| nora.reyes@mailbox.example | Nora Reyes | Louisville | KY | 2021-10-06 | Yes | 1 |
| nora.zimmerman72@inbox.example | Nora Zimmerman | Boise | ID | 2023-12-06 | No | 1 |
| olivia.anderson52@mailbox.example | Olivia Anderson | Miami | FL | 2024-04-05 | Yes | 1 |
| olivia.carter39@mailbox.example | Olivia Carter | Baltimore | MD | 2022-12-10 | No | 1 |
| olivia.ellis13@inbox.example | Olivia Ellis | Charlotte | NC | 2023-12-08 | No | 1 |
| olivia.hughes22@webmail.example | Olivia Hughes | San Francisco | CA | 2026-08-05 | No | 1 |
| olivia.hughes41@inbox.example | Olivia Hughes | Louisville | KY | 2024-08-06 | Yes | 1 |
| olivia.jackson@inbox.example | Olivia Jackson | Tampa | FL | 2024-05-13 | Yes | 1 |
| olivia.kelly@inbox.example | Olivia Kelly | Boston | MA | 2022-03-07 | Yes | 1 |
| olivia.novak51@webmail.example | Olivia Novak | Chicago | IL | 2026-06-27 | No | 1 |
| olivia.perry@webmail.example | Olivia Perry | San Diego | CA | 2021-12-28 | Yes | 1 |
| olivia.quinn@webmail.example | Olivia Quinn | Las Vegas | NV | 2023-10-11 | Yes | 1 |
| olivia.sanders@webmail.example | Olivia Sanders | Houston | TX | 2026-05-28 | Yes | 1 |
| olivia.yamamoto@mailbox.example | Olivia Yamamoto | New Orleans | LA | 2024-02-11 | No | 1 |
| omar.daniels47@inbox.example | Omar Daniels | Seattle | WA | 2026-03-06 | No | 1 |
| omar.daniels73@mailbox.example | Omar Daniels | Los Angeles | CA | 2025-12-12 | Yes | 3 |
| omar.johnson@inbox.example | Omar Johnson | Albuquerque | NM | 2023-12-10 | Yes | 1 |
| omar.kelly90@mailbox.example | Omar Kelly | Minneapolis | MN | 2021-10-19 | No | 2 |
| omar.morgan99@mailbox.example | Omar Morgan | Phoenix | AZ | 2022-08-20 | No | 2 |
| owen.bennett24@webmail.example | Owen Bennett | Dallas | TX | 2021-09-22 | Yes | 2 |
| owen.campbell69@webmail.example | Owen Campbell | Oklahoma City | OK | 2026-04-13 | No | 1 |
| owen.carter56@mailbox.example | Owen Carter | Charlotte | NC | 2022-04-14 | Yes | 3 |
| owen.morgan@inbox.example | Owen Morgan | Charlotte | NC | 2026-05-26 | No | 3 |
| owen.nelson@inbox.example | Owen Nelson | Milwaukee | WI | 2021-10-28 | No | 1 |
| owen.nguyen@mailbox.example | Owen Nguyen | Richmond | VA | 2022-11-07 | Yes | 1 |
| owen.ortiz41@mailbox.example | Owen Ortiz | Milwaukee | WI | 2025-08-08 | No | 1 |
| owen.ramirez@webmail.example | Owen Ramirez | Boston | MA | 2022-03-04 | Yes | 1 |
| owen.reyes@inbox.example | Owen Reyes | San Francisco | CA | 2026-07-18 | Yes | 1 |
| owen.reyes@mailbox.example | Owen Reyes | Indianapolis | IN | 2026-08-26 | No | 1 |
| owen.sanders@mailbox.example | Owen Sanders | Portland | ME | 2025-12-19 | No | 2 |
| owen.walker@mailbox.example | Owen Walker | Kansas City | MO | 2021-11-25 | Yes | 1 |
| owen.xu60@inbox.example | Owen Xu | Portland | ME | 2022-04-24 | No | 1 |
| owen.young64@inbox.example | Owen Young | Columbus | OH | 2023-08-30 | No | 2 |
| priya.flores98@mailbox.example | Priya Flores | Buffalo | NY | 2026-04-29 | No | 2 |
| priya.garcia45@webmail.example | Priya Garcia | Cleveland | OH | 2025-09-25 | No | 1 |
| priya.gupta@inbox.example | Priya Gupta | Des Moines | IA | 2021-08-12 | No | 1 |
| priya.harris@mailbox.example | Priya Harris | Anchorage | AK | 2025-04-15 | No | 3 |
| priya.ingram18@inbox.example | Priya Ingram | San Francisco | CA | 2026-02-06 | Yes | 1 |
| priya.jensen@mailbox.example | Priya Jensen | Milwaukee | WI | 2023-03-23 | Yes | 1 |
| priya.jensen@webmail.example | Priya Jensen | Cleveland | OH | 2024-08-31 | Yes | 2 |
| priya.larson21@inbox.example | Priya Larson | Washington | DC | 2025-01-14 | No | 1 |
| priya.owens@mailbox.example | Priya Owens | Nashville | TN | 2026-06-24 | No | 1 |
| priya.perry@webmail.example | Priya Perry | Portland | ME | 2023-02-08 | No | 2 |
| priya.petrov89@inbox.example | Priya Petrov | Omaha | NE | 2022-05-06 | No | 2 |
| priya.quinn@inbox.example | Priya Quinn | Detroit | MI | 2024-04-05 | No | 1 |
| priya.reyes44@webmail.example | Priya Reyes | Washington | DC | 2025-03-18 | Yes | 1 |
| priya.reyes@webmail.example | Priya Reyes | Anchorage | AK | 2023-02-04 | No | 1 |
| priya.walker29@mailbox.example | Priya Walker | Portland | OR | 2026-07-19 | Yes | 1 |
| priya.xu38@mailbox.example | Priya Xu | Portland | ME | 2024-02-03 | No | 1 |
| rachel.campbell80@inbox.example | Rachel Campbell | Buffalo | NY | 2026-05-16 | No | 1 |
| rachel.daniels91@mailbox.example | Rachel Daniels | San Francisco | CA | 2024-05-04 | No | 1 |
| rachel.hammond@mailbox.example | Rachel Hammond | Albuquerque | NM | 2021-08-17 | No | 1 |
| rachel.harris@webmail.example | Rachel Harris | Minneapolis | MN | 2025-08-03 | Yes | 2 |
| rachel.nguyen@mailbox.example | Rachel Nguyen | Atlanta | GA | 2024-11-01 | No | 1 |
| rachel.quinn@inbox.example | Rachel Quinn | Denver | CO | 2024-05-23 | Yes | 1 |
| rachel.vasquez99@inbox.example | Rachel Vasquez | San Diego | CA | 2023-04-01 | Yes | 1 |
| scarlett.bishop@mailbox.example | Scarlett Bishop | Detroit | MI | 2023-07-17 | Yes | 1 |
| scarlett.garcia45@webmail.example | Scarlett Garcia | Seattle | WA | 2023-06-16 | Yes | 1 |
| scarlett.hughes@inbox.example | Scarlett Hughes | Atlanta | GA | 2022-04-10 | Yes | 1 |
| scarlett.ingram4@inbox.example | Scarlett Ingram | Des Moines | IA | 2024-04-20 | Yes | 1 |
| scarlett.johnson83@mailbox.example | Scarlett Johnson | Portland | OR | 2024-11-09 | Yes | 1 |
| scarlett.patel48@inbox.example | Scarlett Patel | Minneapolis | MN | 2021-11-02 | Yes | 1 |
| scarlett.ramirez44@inbox.example | Scarlett Ramirez | Atlanta | GA | 2022-07-15 | No | 1 |
| scarlett.singh@webmail.example | Scarlett Singh | Phoenix | AZ | 2024-04-03 | No | 1 |
| scarlett.thompson@mailbox.example | Scarlett Thompson | Omaha | NE | 2022-09-18 | No | 2 |
| scarlett.walker43@mailbox.example | Scarlett Walker | Des Moines | IA | 2026-05-10 | Yes | 1 |
| scarlett.walker@inbox.example | Scarlett Walker | Washington | DC | 2023-09-25 | Yes | 1 |
| scarlett.young@inbox.example | Scarlett Young | Boston | MA | 2024-12-09 | Yes | 2 |
| scarlett.zimmerman@inbox.example | Scarlett Zimmerman | Louisville | KY | 2026-04-12 | Yes | 1 |
| scarlett.zimmerman@mailbox.example | Scarlett Zimmerman | Las Vegas | NV | 2025-12-07 | No | 1 |
| sophia.donovan@inbox.example | Sophia Donovan | Louisville | KY | 2023-09-05 | Yes | 1 |
| sophia.gray84@mailbox.example | Sophia Gray | Baltimore | MD | 2023-07-18 | No | 2 |
| sophia.gupta45@webmail.example | Sophia Gupta | Albuquerque | NM | 2022-02-22 | No | 1 |
| sophia.ingram94@inbox.example | Sophia Ingram | Pittsburgh | PA | 2024-07-07 | No | 1 |
| sophia.johnson27@mailbox.example | Sophia Johnson | Houston | TX | 2024-08-01 | No | 2 |
| sophia.larson@webmail.example | Sophia Larson | Denver | CO | 2026-05-13 | Yes | 3 |
| sophia.patel66@inbox.example | Sophia Patel | Boston | MA | 2022-04-27 | No | 1 |
| sophia.patel@webmail.example | Sophia Patel | Denver | CO | 2022-09-21 | No | 1 |
| soren.alvarez@inbox.example | Soren Alvarez | Louisville | KY | 2026-04-09 | Yes | 1 |
| soren.carter@mailbox.example | Soren Carter | Denver | CO | 2026-04-24 | Yes | 1 |
| soren.foster9@mailbox.example | Soren Foster | Oklahoma City | OK | 2023-08-06 | No | 1 |
| soren.gupta28@webmail.example | Soren Gupta | Orlando | FL | 2026-07-20 | No | 1 |
| soren.jackson@webmail.example | Soren Jackson | Los Angeles | CA | 2024-07-07 | Yes | 1 |
| soren.lopez88@webmail.example | Soren Lopez | Phoenix | AZ | 2022-10-11 | Yes | 1 |
| soren.mitchell@mailbox.example | Soren Mitchell | Austin | TX | 2026-04-13 | Yes | 1 |
| soren.novak90@inbox.example | Soren Novak | Omaha | NE | 2023-10-06 | Yes | 1 |
| soren.owens@inbox.example | Soren Owens | Portland | ME | 2023-06-03 | No | 2 |
| soren.perry93@webmail.example | Soren Perry | Oklahoma City | OK | 2023-08-31 | Yes | 1 |
| soren.walker@webmail.example | Soren Walker | Portland | OR | 2022-03-11 | Yes | 1 |
| tamara.bishop@webmail.example | Tamara Bishop | Des Moines | IA | 2023-01-25 | No | 1 |
| tamara.campbell@webmail.example | Tamara Campbell | Oklahoma City | OK | 2022-10-22 | No | 1 |
| tamara.donovan@mailbox.example | Tamara Donovan | Houston | TX | 2024-05-31 | Yes | 1 |
| tamara.edwards59@mailbox.example | Tamara Edwards | Cleveland | OH | 2022-01-27 | No | 1 |
| tamara.ingram80@inbox.example | Tamara Ingram | Atlanta | GA | 2025-01-03 | Yes | 1 |
| tamara.jackson@inbox.example | Tamara Jackson | Los Angeles | CA | 2025-10-21 | No | 1 |
| tamara.kowalski@mailbox.example | Tamara Kowalski | Omaha | NE | 2026-08-25 | No | 1 |
| tamara.nelson57@inbox.example | Tamara Nelson | Los Angeles | CA | 2022-11-05 | Yes | 1 |
| tamara.nguyen@mailbox.example | Tamara Nguyen | Los Angeles | CA | 2026-01-06 | No | 2 |
| tamara.reyes@mailbox.example | Tamara Reyes | Houston | TX | 2025-01-01 | No | 1 |
| tamara.rossi@inbox.example | Tamara Rossi | Austin | TX | 2023-07-18 | Yes | 2 |
| tamara.sanders31@inbox.example | Tamara Sanders | Phoenix | AZ | 2025-05-04 | Yes | 1 |
| tamara.singh@inbox.example | Tamara Singh | Oklahoma City | OK | 2026-02-27 | Yes | 1 |
| tamara.vasquez@webmail.example | Tamara Vasquez | Houston | TX | 2025-12-08 | No | 2 |
| tamara.walsh64@inbox.example | Tamara Walsh | Providence | RI | 2026-09-12 | Yes | 1 |
| tamara.xu@inbox.example | Tamara Xu | Honolulu | HI | 2023-11-10 | No | 1 |
| tamara.xu@mailbox.example | Tamara Xu | Charlotte | NC | 2022-05-13 | No | 1 |
| tessa.brooks@webmail.example | Tessa Brooks | Milwaukee | WI | 2021-11-04 | No | 1 |
| tessa.carter@inbox.example | Tessa Carter | Milwaukee | WI | 2023-04-30 | Yes | 1 |
| tessa.edwards1@webmail.example | Tessa Edwards | Tampa | FL | 2026-04-08 | Yes | 1 |
| tessa.edwards7@mailbox.example | Tessa Edwards | Las Vegas | NV | 2024-01-16 | No | 1 |
| tessa.jackson17@webmail.example | Tessa Jackson | Philadelphia | PA | 2023-08-01 | No | 1 |
| tessa.kim10@mailbox.example | Tessa Kim | Denver | CO | 2023-10-30 | Yes | 1 |
| tessa.mitchell81@inbox.example | Tessa Mitchell | Honolulu | HI | 2025-01-27 | Yes | 1 |
| tessa.nelson42@inbox.example | Tessa Nelson | Minneapolis | MN | 2025-10-27 | Yes | 1 |
| tessa.quinn@mailbox.example | Tessa Quinn | Albuquerque | NM | 2024-07-14 | Yes | 7 |
| tessa.sanders83@inbox.example | Tessa Sanders | Charlotte | NC | 2022-08-04 | Yes | 2 |
| tessa.zimmerman@mailbox.example | Tessa Zimmerman | Portland | OR | 2021-09-27 | No | 2 |
| wyatt.davis1@webmail.example | Wyatt Davis | Raleigh | NC | 2023-09-11 | No | 1 |
| wyatt.ingram@mailbox.example | Wyatt Ingram | Washington | DC | 2024-07-04 | No | 1 |
| wyatt.jensen@inbox.example | Wyatt Jensen | Washington | DC | 2024-08-25 | No | 3 |
| wyatt.kelly@mailbox.example | Wyatt Kelly | Kansas City | MO | 2024-04-08 | Yes | 1 |
| wyatt.nelson66@mailbox.example | Wyatt Nelson | Nashville | TN | 2023-08-17 | Yes | 1 |
| wyatt.okafor@mailbox.example | Wyatt Okafor | Atlanta | GA | 2026-08-05 | Yes | 2 |
| wyatt.patel27@webmail.example | Wyatt Patel | Anchorage | AK | 2023-07-18 | Yes | 1 |
| wyatt.patel@webmail.example | Wyatt Patel | Los Angeles | CA | 2022-01-04 | Yes | 1 |
| wyatt.reyes21@inbox.example | Wyatt Reyes | Anchorage | AK | 2021-11-30 | No | 4 |
| wyatt.sanders@mailbox.example | Wyatt Sanders | Albuquerque | NM | 2026-07-23 | Yes | 1 |
| wyatt.xu@inbox.example | Wyatt Xu | Detroit | MI | 2024-04-04 | Yes | 1 |
| zoey.carter95@inbox.example | Zoey Carter | Detroit | MI | 2025-03-15 | No | 2 |
| zoey.ellis36@webmail.example | Zoey Ellis | Providence | RI | 2024-09-08 | No | 3 |
| zoey.gupta@mailbox.example | Zoey Gupta | Raleigh | NC | 2025-02-25 | No | 1 |
| zoey.hughes@webmail.example | Zoey Hughes | Las Vegas | NV | 2026-05-29 | Yes | 1 |
| zoey.kowalski@inbox.example | Zoey Kowalski | Orlando | FL | 2025-11-09 | Yes | 1 |
| zoey.nelson53@webmail.example | Zoey Nelson | Dallas | TX | 2025-11-10 | No | 1 |
| zoey.ortiz77@mailbox.example | Zoey Ortiz | Milwaukee | WI | 2022-04-17 | Yes | 3 |
| zoey.petrov@inbox.example | Zoey Petrov | San Francisco | CA | 2025-05-24 | No | 1 |
| zoey.sanders69@inbox.example | Zoey Sanders | Washington | DC | 2026-07-16 | Yes | 1 |
| zoey.underwood@webmail.example | Zoey Underwood | Oklahoma City | OK | 2026-04-08 | No | 1 |
| zoey.zimmerman@inbox.example | Zoey Zimmerman | Richmond | VA | 2022-02-05 | Yes | 3 |
| zoey.zimmerman@webmail.example | Zoey Zimmerman | Indianapolis | IN | 2023-08-08 | No | 1 |

## Order ledger

| Order ID | Placed (ET) | Email | Ship to | Items | Subtotal | Shipping | Total | Payment | Shipping option | Status | Related records | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| JL-10001 | 2026-06-01 14:33 | isaac.garcia72@inbox.example | Richmond, VA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10002 | 2026-06-01 16:34 | tessa.quinn@mailbox.example | Albuquerque, NM | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10003 | 2026-06-01 19:35 | tessa.quinn@mailbox.example | Albuquerque, NM | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | — | — |
| JL-10004 | 2026-06-01 19:42 | lucas.quinn@mailbox.example | Baltimore, MD | Personalised Leather Notebook ×1 (emboss "A. Rivera") | $29.00 | $4.99 | $33.99 | Visa | Standard | delivered | — | — |
| JL-10005 | 2026-06-01 21:02 | lucas.quinn@mailbox.example | Baltimore, MD | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | WC-40011 | — |
| JL-10006 | 2026-06-01 21:23 | lucas.quinn@mailbox.example | Baltimore, MD | Linen Napkins (Set of 4) ×2 | $37.00 | $12.99 | $49.99 | Visa | Express | delivered | — | — |
| JL-10007 | 2026-06-02 04:05 | owen.young64@inbox.example | Columbus, OH | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10008 | 2026-06-02 10:06 | evelyn.ingram37@mailbox.example | Portland, ME | Bamboo Cutting Board ×1; LED Desk Lamp ×1 | $58.50 | $12.99 | $71.49 | Mastercard | Express | delivered | — | — |
| JL-10009 | 2026-06-02 11:24 | mason.alvarez79@inbox.example | Milwaukee, WI | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | PayPal | Standard | delivered | — | — |
| JL-10010 | 2026-06-02 11:26 | ingrid.quinn79@webmail.example | Detroit, MI | Linen Napkins (Set of 4) ×1 | $18.50 | $12.99 | $31.49 | Visa | Express | delivered | — | — |
| JL-10011 | 2026-06-02 11:48 | mia.bennett34@webmail.example | Austin, TX | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | American Express | Standard | delivered | RT-20013 | — |
| JL-10012 | 2026-06-02 13:02 | mia.gupta@inbox.example | New York, NY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10013 | 2026-06-02 13:38 | aaliyah.ortiz@webmail.example | Los Angeles, CA | Ceramic Pour-Over Coffee Set ×1; Scented Soy Candle ×1 | $54.00 | $0.00 | $54.00 | Mastercard | Standard | delivered | — | — |
| JL-10014 | 2026-06-02 15:19 | priya.flores98@mailbox.example | Buffalo, NY | Wireless Earbuds Pro ×1; Electric Kettle 1.7L ×1 | $124.00 | $0.00 | $124.00 | Mastercard | Standard | cancelled | RF-30001 | Cancelled 2026-06-03 11:03: Customer request — changed mind |
| JL-10015 | 2026-06-03 06:49 | aaliyah.ortiz@webmail.example | Los Angeles, CA | Wireless Earbuds Pro ×1; Ceramic Planter Set ×1 | $111.00 | $12.99 | $123.99 | Visa | Express | delivered | — | — |
| JL-10016 | 2026-06-03 09:39 | ethan.reyes@inbox.example | Seattle, WA | Oak Side Table ×1; Bluetooth Speaker Mini ×1 | $168.99 | $0.00 | $168.99 | PayPal | Standard | delivered | — | — |
| JL-10017 | 2026-06-03 10:43 | diego.daniels49@mailbox.example | Indianapolis, IN | Oak Side Table ×1; Linen Napkins (Set of 4) ×1; LED Desk Lamp ×2 | $216.50 | $0.00 | $216.50 | Visa | Standard | delivered | — | — |
| JL-10018 | 2026-06-03 11:03 | liam.bennett@webmail.example | Oklahoma City, OK | Oak Side Table ×1; Bamboo Cutting Board ×1 | $153.00 | $0.00 | $153.00 | Mastercard | Standard | delivered | — | — |
| JL-10019 | 2026-06-03 12:06 | isaac.garcia72@inbox.example | Richmond, VA | Smart Plug (2-Pack) ×1 | $25.00 | $12.99 | $37.99 | Mastercard | Express | delivered | — | — |
| JL-10020 | 2026-06-03 13:17 | devon.johnson87@mailbox.example | Charlotte, NC | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | cancelled | RF-30002 | Cancelled 2026-06-03 15:25: Customer request — changed mind |
| JL-10021 | 2026-06-03 13:45 | logan.garcia@inbox.example | New Orleans, LA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | — | — |
| JL-10022 | 2026-06-03 14:05 | isaac.garcia72@inbox.example | Richmond, VA | Bluetooth Speaker Mini ×3 | $119.97 | $0.00 | $119.97 | Visa | Standard | delivered | — | — |
| JL-10023 | 2026-06-03 18:50 | tessa.quinn@mailbox.example | Albuquerque, NM | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10024 | 2026-06-03 20:44 | aaliyah.daniels17@webmail.example | Baltimore, MD | Wool Throw Blanket ×1 | $68.00 | $12.99 | $80.99 | PayPal | Express | delivered | — | — |
| JL-10025 | 2026-06-04 14:48 | brandon.bishop@mailbox.example | Salt Lake City, UT | Personalised Leather Notebook ×1 (emboss "J\&M 2026"); Scented Soy Candle ×1 | $41.00 | $4.99 | $45.99 | Visa | Standard | delivered | INV-50002 | — |
| JL-10026 | 2026-06-04 19:13 | lucia.petrov51@mailbox.example | Washington, DC | Adjustable Phone Stand ×1; Linen Napkins (Set of 4) ×2 | $52.00 | $0.00 | $52.00 | Visa | Standard | delivered | RT-20005, RF-30016 | — |
| JL-10027 | 2026-06-05 05:50 | zoey.carter95@inbox.example | Detroit, MI | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | American Express | Email (digital) | delivered | — | — |
| JL-10028 | 2026-06-05 08:11 | maya.lopez39@inbox.example | Honolulu, HI | LED Desk Lamp ×2; Wireless Earbuds Pro ×1 | $148.00 | $0.00 | $148.00 | American Express | Standard | delivered | — | — |
| JL-10029 | 2026-06-05 10:06 | owen.bennett24@webmail.example | Dallas, TX | LED Desk Lamp ×1; Smart Plug (2-Pack) ×1 | $59.50 | $0.00 | $59.50 | Mastercard | Standard | delivered | — | — |
| JL-10030 | 2026-06-05 10:15 | ethan.turner96@mailbox.example | Louisville, KY | Adjustable Phone Stand ×1; Bamboo Cutting Board ×1; Wireless Earbuds Pro ×1 | $118.00 | $0.00 | $118.00 | Mastercard | Standard | delivered | RT-20010, RF-30034 | — |
| JL-10031 | 2026-06-05 12:20 | arjun.zimmerman79@webmail.example | Phoenix, AZ | Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam"); Wireless Earbuds Pro ×1; Adjustable Phone Stand ×1 | $152.00 | $0.00 | $152.00 | Visa | Standard | delivered | RT-20002 | — |
| JL-10032 | 2026-06-05 13:58 | jamal.harris@inbox.example | Louisville, KY | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | cancelled | RF-30003 | Cancelled 2026-06-05 14:04: Customer request — ordered wrong item |
| JL-10033 | 2026-06-05 14:36 | ella.donovan60@mailbox.example | Nashville, TN | Wireless Earbuds Pro ×3; Electric Kettle 1.7L ×1 | $282.00 | $0.00 | $282.00 | Mastercard | Standard | delivered | RT-20011, RF-30028 | Delivered after estimated window |
| JL-10034 | 2026-06-05 16:49 | priya.flores98@mailbox.example | Buffalo, NY | Cast Iron Skillet ×1; Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "Thank you, Ms. P") | $96.00 | $12.99 | $108.99 | Visa | Express | delivered | WC-40018 | — |
| JL-10035 | 2026-06-06 04:19 | aaliyah.ortiz@webmail.example | Los Angeles, CA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | RT-20008, RF-30022 | — |
| JL-10036 | 2026-06-06 08:23 | brandon.perry@inbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Wireless Earbuds Pro ×1; Scented Soy Candle ×1 | $115.00 | $12.99 | $127.99 | Visa | Express | delivered | WC-40014 | — |
| JL-10037 | 2026-06-06 08:56 | hiro.ellis@mailbox.example | Boston, MA | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10038 | 2026-06-06 15:36 | mia.nelson@webmail.example | Dallas, TX | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | WC-40006 | — |
| JL-10039 | 2026-06-06 18:06 | brandon.hammond23@mailbox.example | Austin, TX | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Visa | Standard | delivered | — | — |
| JL-10040 | 2026-06-06 19:32 | amelia.daniels94@mailbox.example | Detroit, MI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | RT-20006, RF-30019 | — |
| JL-10041 | 2026-06-06 23:19 | brandon.hammond23@mailbox.example | Austin, TX | Linen Napkins (Set of 4) ×3 | $55.50 | $12.99 | $68.49 | Visa | Express | delivered | — | — |
| JL-10042 | 2026-06-07 04:45 | marcus.kim@webmail.example | Des Moines, IA | Ceramic Pour-Over Coffee Set ×2; Bluetooth Speaker Mini ×1 | $123.99 | $0.00 | $123.99 | Visa | Standard | delivered | WC-40043 | — |
| JL-10043 | 2026-06-07 08:49 | dylan.chen@mailbox.example | Dallas, TX | Linen Napkins (Set of 4) ×2 | $37.00 | $4.99 | $41.99 | Visa | Standard | delivered | — | — |
| JL-10044 | 2026-06-07 10:08 | mei.daniels@inbox.example | Philadelphia, PA | Bluetooth Speaker Mini ×1; Linen Napkins (Set of 4) ×1; Bamboo Cutting Board ×1; Oak Side Table ×1 | $211.49 | $0.00 | $211.49 | PayPal | Standard | delivered | — | — |
| JL-10045 | 2026-06-07 10:57 | julian.johnson44@webmail.example | Nashville, TN | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | PayPal | Standard | delivered | — | — |
| JL-10046 | 2026-06-07 17:31 | grace.quinn@mailbox.example | Nashville, TN | Wireless Earbuds Pro ×3; Smart Plug (2-Pack) ×2; Wool Throw Blanket ×1 | $355.00 | $0.00 | $355.00 | Mastercard | Standard | delivered | RF-30133, WC-40020 | — |
| JL-10047 | 2026-06-07 20:09 | tamara.xu@inbox.example | Honolulu, HI | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | PayPal | Express | delivered | — | — |
| JL-10048 | 2026-06-07 21:40 | ava.gray@webmail.example | Seattle, WA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $12.99 | $54.99 | Visa | Express | delivered | — | — |
| JL-10049 | 2026-06-08 06:29 | liam.nelson11@webmail.example | Las Vegas, NV | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Visa | Express | delivered | — | — |
| JL-10050 | 2026-06-08 11:18 | lucia.novak@webmail.example | Indianapolis, IN | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | WC-40003 | — |
| JL-10051 | 2026-06-08 11:33 | tamara.sanders31@inbox.example | Phoenix, AZ | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Juniper Lane gift card | Standard | delivered | RT-20025 | — |
| JL-10052 | 2026-06-08 15:10 | jackson.quinn@inbox.example | San Francisco, CA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10053 | 2026-06-08 16:32 | aaliyah.kim@mailbox.example | Buffalo, NY | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10054 | 2026-06-08 17:16 | dylan.foster@mailbox.example | Baltimore, MD | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Mastercard | Standard | delivered | — | — |
| JL-10055 | 2026-06-08 20:01 | tessa.quinn@mailbox.example | Albuquerque, NM | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Visa | Express | cancelled | RF-30004 | Cancelled 2026-06-08 22:58: Customer request — ordered wrong item |
| JL-10056 | 2026-06-08 21:21 | maya.chen@inbox.example | Louisville, KY | Cast Iron Skillet ×2; Ceramic Planter Set ×1; Bamboo Cutting Board ×3; Wool Throw Blanket ×3 | $418.00 | $12.99 | $430.99 | PayPal | Express | delivered | — | — |
| JL-10057 | 2026-06-08 22:00 | mason.gupta52@mailbox.example | Pittsburgh, PA | Wool Throw Blanket ×1; Electric Kettle 1.7L ×1 | $113.00 | $0.00 | $113.00 | American Express | Standard | delivered | — | — |
| JL-10058 | 2026-06-09 06:19 | noah.jensen@mailbox.example | Dallas, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | lost | RF-30009, INV-50001 | — |
| JL-10059 | 2026-06-09 09:06 | aaliyah.ortiz@webmail.example | Los Angeles, CA | Linen Napkins (Set of 4) ×1; Personalised Leather Notebook ×1 (emboss "Dad") | $47.50 | $12.99 | $60.49 | American Express | Express | delivered | — | — |
| JL-10060 | 2026-06-09 13:44 | nathan.kowalski@inbox.example | Richmond, VA | Cast Iron Skillet ×1 | $55.00 | $12.99 | $67.99 | Mastercard | Express | delivered | — | — |
| JL-10061 | 2026-06-09 19:22 | chloe.quinn77@webmail.example | Portland, ME | LED Desk Lamp ×1; Linen Napkins (Set of 4) ×1 | $53.00 | $0.00 | $53.00 | Visa | Standard | delivered | WC-40044 | — |
| JL-10062 | 2026-06-09 21:34 | caleb.edwards@webmail.example | Miami, FL | LED Desk Lamp ×1; Wool Throw Blanket ×1 | $102.50 | $0.00 | $102.50 | Mastercard | Standard | delivered | RT-20018, RF-30029 | — |
| JL-10063 | 2026-06-10 10:54 | priya.gupta@inbox.example | Des Moines, IA | Oak Side Table ×1; Smart Plug (2-Pack) ×1 | $154.00 | $0.00 | $154.00 | PayPal | Standard | delivered | — | — |
| JL-10064 | 2026-06-10 12:56 | tessa.quinn@mailbox.example | Albuquerque, NM | Smart Plug (2-Pack) ×1; Electric Kettle 1.7L ×1; Adjustable Phone Stand ×1 | $85.00 | $0.00 | $85.00 | Visa | Standard | delivered | RT-20003, RF-30012 | — |
| JL-10065 | 2026-06-10 14:00 | evelyn.ingram37@mailbox.example | Portland, ME | Scented Soy Candle ×1; Wool Throw Blanket ×1 | $80.00 | $0.00 | $80.00 | Mastercard | Standard | delivered | WC-40071 | Delivered after estimated window |
| JL-10066 | 2026-06-10 14:29 | lucia.petrov51@mailbox.example | Washington, DC | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Mastercard | Standard | delivered | — | — |
| JL-10067 | 2026-06-10 14:39 | gabriel.vasquez@webmail.example | Detroit, MI | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10068 | 2026-06-11 09:00 | chloe.gupta75@mailbox.example | Raleigh, NC | Adjustable Phone Stand ×2; Smart Plug (2-Pack) ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | cancelled | RF-30005 | Cancelled 2026-06-11 14:16: Customer request — ordered wrong item |
| JL-10069 | 2026-06-11 09:51 | omar.daniels73@mailbox.example | Los Angeles, CA | Personalised Leather Notebook ×1 (emboss "Ben's Notes") | $29.00 | $4.99 | $33.99 | Visa | Standard | delivered | — | — |
| JL-10070 | 2026-06-11 14:33 | ava.vasquez@mailbox.example | Los Angeles, CA | Adjustable Phone Stand ×1; Cast Iron Skillet ×1 | $70.00 | $0.00 | $70.00 | Visa | Standard | delivered | — | — |
| JL-10071 | 2026-06-11 16:27 | aiden.gray47@mailbox.example | Honolulu, HI | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | RF-30010, DMG-55001 | — |
| JL-10072 | 2026-06-11 17:25 | mia.gupta@inbox.example | New York, NY | Wool Throw Blanket ×2; Linen Napkins (Set of 4) ×3 | $191.50 | $0.00 | $191.50 | Juniper Lane gift card | Standard | delivered | RT-20004, RF-30020 | — |
| JL-10073 | 2026-06-11 17:37 | emma.edwards38@webmail.example | Cleveland, OH | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | American Express | Standard | delivered | — | — |
| JL-10074 | 2026-06-11 20:40 | gabriel.alvarez@mailbox.example | Orlando, FL | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10075 | 2026-06-12 10:42 | zoey.carter95@inbox.example | Detroit, MI | LED Desk Lamp ×1 | $34.50 | $12.99 | $47.49 | Visa | Express | delivered | RT-20001 | — |
| JL-10076 | 2026-06-12 11:18 | owen.carter56@mailbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Adjustable Phone Stand ×3; Scented Soy Candle ×1 | $81.00 | $12.99 | $93.99 | Visa | Express | delivered | — | — |
| JL-10077 | 2026-06-12 13:50 | nora.bishop@inbox.example | Columbus, OH | Wireless Earbuds Pro ×2; Bluetooth Speaker Mini ×1; Adjustable Phone Stand ×3 | $242.99 | $12.99 | $255.98 | Mastercard | Express | delivered | — | — |
| JL-10078 | 2026-06-12 19:53 | tessa.jackson17@webmail.example | Philadelphia, PA | LED Desk Lamp ×1; Ceramic Planter Set ×1 | $66.50 | $0.00 | $66.50 | Visa | Standard | delivered | — | — |
| JL-10079 | 2026-06-12 20:12 | gabriel.alvarez@mailbox.example | Orlando, FL | LED Desk Lamp ×3 | $103.50 | $12.99 | $116.49 | Visa | Express | delivered | — | — |
| JL-10080 | 2026-06-12 20:42 | emma.flores@mailbox.example | Milwaukee, WI | Cast Iron Skillet ×3; Scented Soy Candle ×1; Ceramic Pour-Over Coffee Set ×2 | $261.00 | $0.00 | $261.00 | Visa | Standard | delivered | RT-20009, RF-30025 | — |
| JL-10081 | 2026-06-12 21:05 | isaac.petrov@mailbox.example | Los Angeles, CA | Wireless Earbuds Pro ×3; Adjustable Phone Stand ×1 | $252.00 | $0.00 | $252.00 | Visa | Standard | delivered | — | — |
| JL-10082 | 2026-06-13 09:52 | keisha.martinez@webmail.example | Providence, RI | Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1 | $64.99 | $0.00 | $64.99 | Visa | Standard | delivered | — | — |
| JL-10083 | 2026-06-13 14:32 | chloe.gupta75@mailbox.example | Raleigh, NC | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10084 | 2026-06-13 16:25 | sophia.johnson27@mailbox.example | Houston, TX | Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1; Electric Kettle 1.7L ×1 | $109.99 | $0.00 | $109.99 | Visa | Standard | delivered | WC-40004 | — |
| JL-10085 | 2026-06-13 16:36 | aiden.xu99@inbox.example | Dallas, TX | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Visa | Express | delivered | — | Delivered after estimated window |
| JL-10086 | 2026-06-13 17:11 | liam.brooks@mailbox.example | Raleigh, NC | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10087 | 2026-06-13 18:35 | lucia.petrov51@mailbox.example | Washington, DC | Smart Plug (2-Pack) ×1; Bamboo Cutting Board ×1; Ceramic Pour-Over Coffee Set ×1 | $91.00 | $12.99 | $103.99 | Mastercard | Express | lost | INV-50003 | — |
| JL-10088 | 2026-06-13 23:48 | tamara.vasquez@webmail.example | Houston, TX | Bamboo Cutting Board ×1; Wireless Earbuds Pro ×2; Bluetooth Speaker Mini ×3 | $301.97 | $0.00 | $301.97 | Juniper Lane gift card | Standard | delivered | WC-40013 | — |
| JL-10089 | 2026-06-14 06:13 | nora.perry47@mailbox.example | Buffalo, NY | Wireless Earbuds Pro ×3 | $237.00 | $0.00 | $237.00 | Juniper Lane gift card | Standard | delivered | WC-40052 | — |
| JL-10090 | 2026-06-14 06:58 | nora.ingram@inbox.example | Anchorage, AK | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10091 | 2026-06-14 07:11 | james.larson@mailbox.example | Chicago, IL | Wireless Earbuds Pro ×2; Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1; Scented Soy Candle ×1 | $234.99 | $0.00 | $234.99 | American Express | Standard | delivered | — | — |
| JL-10092 | 2026-06-14 12:39 | tamara.vasquez@webmail.example | Houston, TX | Electric Kettle 1.7L ×1; Wireless Earbuds Pro ×1 | $124.00 | $12.99 | $136.99 | Juniper Lane gift card | Express | delivered | WC-40009 | — |
| JL-10093 | 2026-06-14 14:51 | evelyn.johnson33@inbox.example | Detroit, MI | LED Desk Lamp ×1 | $34.50 | $12.99 | $47.49 | Mastercard | Express | lost | RF-30014, INV-50004 | — |
| JL-10094 | 2026-06-14 14:59 | mateo.harris20@inbox.example | Los Angeles, CA | Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam"); Wool Throw Blanket ×1; Ceramic Pour-Over Coffee Set ×1 | $168.00 | $12.99 | $180.99 | Mastercard | Express | delivered | — | — |
| JL-10095 | 2026-06-14 15:27 | priya.petrov89@inbox.example | Omaha, NE | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10096 | 2026-06-14 16:48 | tessa.zimmerman@mailbox.example | Portland, OR | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | American Express | Standard | cancelled | RF-30006 | Cancelled 2026-06-15 04:39: Customer request — ordered wrong item |
| JL-10097 | 2026-06-14 18:23 | scarlett.thompson@mailbox.example | Omaha, NE | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10098 | 2026-06-14 18:53 | evelyn.ingram37@mailbox.example | Portland, ME | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | PayPal | Express | delivered | — | — |
| JL-10099 | 2026-06-14 19:48 | ava.turner67@webmail.example | Salt Lake City, UT | Electric Kettle 1.7L ×3 | $135.00 | $0.00 | $135.00 | Visa | Standard | delivered | — | — |
| JL-10100 | 2026-06-15 08:17 | aaliyah.alvarez34@mailbox.example | Richmond, VA | Linen Napkins (Set of 4) ×1 | $18.50 | $12.99 | $31.49 | American Express | Express | delivered | — | — |
| JL-10101 | 2026-06-15 19:06 | lucia.patel@webmail.example | Burlington, VT | Bluetooth Speaker Mini ×1; Wireless Earbuds Pro ×2 | $197.99 | $0.00 | $197.99 | Mastercard | Standard | delivered | — | — |
| JL-10102 | 2026-06-16 02:09 | lily.zimmerman50@webmail.example | Orlando, FL | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Mastercard | Express | delivered | — | — |
| JL-10103 | 2026-06-16 15:29 | aria.kelly@webmail.example | Pittsburgh, PA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10104 | 2026-06-16 16:32 | caleb.hammond80@webmail.example | Las Vegas, NV | Electric Kettle 1.7L ×1; Linen Napkins (Set of 4) ×1 | $63.50 | $0.00 | $63.50 | Mastercard | Standard | cancelled | RF-30008 | Cancelled 2026-06-17 13:49: Customer request — ordered wrong item |
| JL-10105 | 2026-06-16 17:41 | abigail.thompson55@webmail.example | Los Angeles, CA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | WC-40001 | — |
| JL-10106 | 2026-06-16 23:43 | isaac.petrov@mailbox.example | Los Angeles, CA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $12.99 | $54.99 | Mastercard | Express | cancelled | RF-30007 | Cancelled 2026-06-16 23:53: Customer request — ordered wrong item |
| JL-10107 | 2026-06-17 04:00 | maya.campbell@inbox.example | Honolulu, HI | Wireless Earbuds Pro ×1; Wool Throw Blanket ×1 | $147.00 | $0.00 | $147.00 | Mastercard | Standard | delivered | — | — |
| JL-10108 | 2026-06-17 05:17 | zoey.ortiz77@mailbox.example | Milwaukee, WI | Bamboo Cutting Board ×1; Wireless Earbuds Pro ×1 | $103.00 | $12.99 | $115.99 | Visa | Express | delivered | WC-40012 | — |
| JL-10109 | 2026-06-17 08:33 | evelyn.sanders96@mailbox.example | Portland, OR | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | American Express | Standard | delivered | — | Delivered after estimated window |
| JL-10110 | 2026-06-17 09:36 | ethan.turner96@mailbox.example | Louisville, KY | Cast Iron Skillet ×1; Bluetooth Speaker Mini ×1 | $94.99 | $0.00 | $94.99 | PayPal | Standard | delivered | RT-20014, RF-30041 | — |
| JL-10111 | 2026-06-17 12:31 | priya.harris@mailbox.example | Anchorage, AK | Electric Kettle 1.7L ×1; Personalised Leather Notebook ×1 (emboss "Team Lead") | $74.00 | $0.00 | $74.00 | PayPal | Standard | lost | INV-50005 | — |
| JL-10112 | 2026-06-17 14:03 | ethan.anderson44@inbox.example | Los Angeles, CA | Linen Napkins (Set of 4) ×1 | $18.50 | $12.99 | $31.49 | Visa | Express | delivered | — | — |
| JL-10113 | 2026-06-18 08:44 | aria.chen@inbox.example | New Orleans, LA | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | American Express | Standard | delivered | — | — |
| JL-10114 | 2026-06-18 18:57 | jamal.novak@webmail.example | Louisville, KY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10115 | 2026-06-18 21:43 | mei.ellis@inbox.example | Charlotte, NC | Linen Napkins (Set of 4) ×2; Wireless Earbuds Pro ×1 | $116.00 | $0.00 | $116.00 | PayPal | Standard | delivered | — | — |
| JL-10116 | 2026-06-19 08:26 | ethan.ellis3@mailbox.example | Oklahoma City, OK | Bamboo Cutting Board ×1; Electric Kettle 1.7L ×1 | $69.00 | $0.00 | $69.00 | Visa | Standard | delivered | — | — |
| JL-10117 | 2026-06-19 09:00 | elijah.gupta@webmail.example | Denver, CO | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10118 | 2026-06-19 18:19 | james.johnson73@mailbox.example | Honolulu, HI | LED Desk Lamp ×2; Wool Throw Blanket ×2; Bamboo Cutting Board ×1 | $229.00 | $0.00 | $229.00 | PayPal | Standard | delivered | — | — |
| JL-10119 | 2026-06-20 01:26 | mei.ellis@inbox.example | Charlotte, NC | Cast Iron Skillet ×1; Linen Napkins (Set of 4) ×2; Adjustable Phone Stand ×1; Smart Plug (2-Pack) ×3 | $182.00 | $0.00 | $182.00 | PayPal | Standard | delivered | WC-40051 | — |
| JL-10120 | 2026-06-20 09:11 | aria.kim21@mailbox.example | Orlando, FL | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | WC-40019 | — |
| JL-10121 | 2026-06-20 11:56 | tessa.quinn@mailbox.example | Albuquerque, NM | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Mastercard | Standard | delivered | — | — |
| JL-10122 | 2026-06-20 14:58 | mateo.singh@inbox.example | Austin, TX | Smart Plug (2-Pack) ×1; Linen Napkins (Set of 4) ×1; Electric Kettle 1.7L ×1 | $88.50 | $0.00 | $88.50 | American Express | Standard | delivered | — | — |
| JL-10123 | 2026-06-20 18:47 | gabriel.foster60@inbox.example | Des Moines, IA | Oak Side Table ×1; Bamboo Cutting Board ×1 | $153.00 | $0.00 | $153.00 | Visa | Standard | delivered | WC-40017 | — |
| JL-10124 | 2026-06-20 20:07 | maya.kim35@mailbox.example | Minneapolis, MN | LED Desk Lamp ×2 | $69.00 | $12.99 | $81.99 | PayPal | Express | delivered | — | — |
| JL-10125 | 2026-06-20 20:39 | lucas.kelly51@inbox.example | Des Moines, IA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | RT-20026 | — |
| JL-10126 | 2026-06-20 21:11 | jamal.young@mailbox.example | Burlington, VT | LED Desk Lamp ×1; Electric Kettle 1.7L ×1; Scented Soy Candle ×3 | $115.50 | $0.00 | $115.50 | Mastercard | Standard | delivered | WC-40038 | — |
| JL-10127 | 2026-06-21 06:17 | maya.bennett@mailbox.example | Omaha, NE | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Mastercard | Express | delivered | RF-30013, DMG-55002 | — |
| JL-10128 | 2026-06-21 09:43 | mei.zimmerman@webmail.example | Chicago, IL | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1; Wireless Earbuds Pro ×1 | $153.49 | $0.00 | $153.49 | Visa | Standard | delivered | RT-20007, RF-30024 | — |
| JL-10129 | 2026-06-21 10:43 | fatima.ellis93@mailbox.example | Providence, RI | Scented Soy Candle ×1; Smart Plug (2-Pack) ×2; Bamboo Cutting Board ×1 | $86.00 | $12.99 | $98.99 | PayPal | Express | delivered | — | Delivered after estimated window |
| JL-10130 | 2026-06-21 10:54 | ava.campbell@webmail.example | Burlington, VT | Ceramic Planter Set ×1; Linen Napkins (Set of 4) ×1 | $50.50 | $0.00 | $50.50 | Visa | Standard | delivered | RT-20016, RF-30036 | — |
| JL-10131 | 2026-06-21 12:25 | lily.zimmerman50@webmail.example | Orlando, FL | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | RT-20027, RF-30050 | — |
| JL-10132 | 2026-06-21 16:15 | jackson.donovan@mailbox.example | Milwaukee, WI | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10133 | 2026-06-21 16:19 | jackson.quinn@inbox.example | San Francisco, CA | Bamboo Cutting Board ×1; Linen Napkins (Set of 4) ×1 | $42.50 | $4.99 | $47.49 | Visa | Standard | delivered | — | — |
| JL-10134 | 2026-06-21 18:29 | aria.kim64@inbox.example | Buffalo, NY | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | — | — |
| JL-10135 | 2026-06-22 14:21 | lucas.davis59@inbox.example | Oklahoma City, OK | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10136 | 2026-06-22 17:08 | mia.turner52@inbox.example | Buffalo, NY | Ceramic Planter Set ×2 | $64.00 | $0.00 | $64.00 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10137 | 2026-06-23 13:17 | liam.nelson11@webmail.example | Las Vegas, NV | Ceramic Pour-Over Coffee Set ×1; Smart Plug (2-Pack) ×1 | $67.00 | $0.00 | $67.00 | Visa | Standard | delivered | RT-20012, RF-30035 | — |
| JL-10138 | 2026-06-23 20:41 | ava.campbell@webmail.example | Burlington, VT | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10139 | 2026-06-23 21:26 | isabella.foster13@inbox.example | Houston, TX | Bluetooth Speaker Mini ×1; Scented Soy Candle ×1; Wireless Earbuds Pro ×1 | $130.99 | $12.99 | $143.98 | Mastercard | Express | delivered | — | Delivered after estimated window |
| JL-10140 | 2026-06-24 12:09 | jackson.donovan@mailbox.example | Milwaukee, WI | Adjustable Phone Stand ×1 | $15.00 | $12.99 | $27.99 | Juniper Lane gift card | Express | delivered | RT-20029, RF-30059 | — |
| JL-10141 | 2026-06-24 12:14 | liam.brooks@mailbox.example | Raleigh, NC | Bamboo Cutting Board ×2 | $48.00 | $4.99 | $52.99 | Mastercard | Standard | delivered | — | — |
| JL-10142 | 2026-06-24 12:57 | omar.daniels47@inbox.example | Seattle, WA | LED Desk Lamp ×1; Bluetooth Speaker Mini ×2 | $114.48 | $0.00 | $114.48 | PayPal | Standard | delivered | WC-40032 | — |
| JL-10143 | 2026-06-24 16:23 | caleb.hammond80@webmail.example | Las Vegas, NV | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | American Express | Express | delivered | — | — |
| JL-10144 | 2026-06-25 02:06 | lily.vasquez@mailbox.example | Cleveland, OH | Oak Side Table ×1; Bluetooth Speaker Mini ×1 | $168.99 | $12.99 | $181.98 | Visa | Express | delivered | — | — |
| JL-10145 | 2026-06-25 02:18 | liam.underwood@mailbox.example | San Francisco, CA | Bluetooth Speaker Mini ×2; Personalised Leather Notebook ×1 (emboss "J\&M 2026") | $108.98 | $0.00 | $108.98 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10146 | 2026-06-25 14:47 | evelyn.ingram37@mailbox.example | Portland, ME | LED Desk Lamp ×2; Ceramic Pour-Over Coffee Set ×2; Cast Iron Skillet ×1 | $208.00 | $12.99 | $220.99 | Visa | Express | delivered | — | — |
| JL-10147 | 2026-06-25 18:36 | wyatt.reyes21@inbox.example | Anchorage, AK | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10148 | 2026-06-25 18:40 | logan.ramirez@mailbox.example | Anchorage, AK | Wireless Earbuds Pro ×1; Wool Throw Blanket ×1 | $147.00 | $0.00 | $147.00 | Visa | Standard | delivered | RT-20015, RF-30042 | — |
| JL-10149 | 2026-06-25 19:01 | mei.larson@mailbox.example | Boise, ID | Bluetooth Speaker Mini ×1; Adjustable Phone Stand ×1 | $54.99 | $0.00 | $54.99 | Visa | Standard | cancelled | RF-30011 | Cancelled 2026-06-26 09:22: Customer request — ordered wrong item |
| JL-10150 | 2026-06-25 19:37 | evelyn.bennett52@mailbox.example | Richmond, VA | Electric Kettle 1.7L ×1; Ceramic Pour-Over Coffee Set ×2 | $129.00 | $0.00 | $129.00 | Mastercard | Standard | delivered | — | — |
| JL-10151 | 2026-06-25 20:34 | devon.johnson87@mailbox.example | Charlotte, NC | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10152 | 2026-06-26 07:08 | julian.owens85@inbox.example | Des Moines, IA | Cast Iron Skillet ×1; Scented Soy Candle ×1 | $67.00 | $0.00 | $67.00 | PayPal | Standard | delivered | — | — |
| JL-10153 | 2026-06-26 07:11 | mason.owens@mailbox.example | Houston, TX | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | PayPal | Standard | delivered | — | — |
| JL-10154 | 2026-06-26 08:41 | tessa.zimmerman@mailbox.example | Portland, OR | Smart Plug (2-Pack) ×1; Cast Iron Skillet ×1 | $80.00 | $12.99 | $92.99 | Visa | Express | delivered | — | — |
| JL-10155 | 2026-06-26 09:49 | isaac.petrov@mailbox.example | Los Angeles, CA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10156 | 2026-06-26 10:49 | ava.martinez@inbox.example | Nashville, TN | Bluetooth Speaker Mini ×1; Electric Kettle 1.7L ×1 | $84.99 | $0.00 | $84.99 | PayPal | Standard | delivered | — | — |
| JL-10157 | 2026-06-26 11:11 | logan.singh@inbox.example | Portland, ME | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Mastercard | Standard | delivered | WC-40002 | — |
| JL-10158 | 2026-06-26 16:23 | ethan.anderson@mailbox.example | Las Vegas, NV | Electric Kettle 1.7L ×1; Wireless Earbuds Pro ×1; Scented Soy Candle ×1 | $136.00 | $0.00 | $136.00 | Visa | Standard | delivered | — | — |
| JL-10159 | 2026-06-26 18:47 | mei.walker52@webmail.example | Richmond, VA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-11001 | 2026-06-27 10:57 | elijah.daniels@inbox.example | Buffalo, NY | LED Desk Lamp ×1; Ceramic Pour-Over Coffee Set ×1; Adjustable Phone Stand ×1 | $91.50 | $0.00 | $91.50 | Visa | Standard | delivered | — | — |
| JL-10161 | 2026-06-27 16:40 | fatima.campbell66@webmail.example | Columbus, OH | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10162 | 2026-06-27 19:29 | omar.daniels73@mailbox.example | Los Angeles, CA | Personalised Leather Notebook ×1 (emboss "For Maya"); Electric Kettle 1.7L ×1 | $74.00 | $0.00 | $74.00 | Visa | Standard | delivered | RT-20019, RF-30040 | — |
| JL-10163 | 2026-06-27 20:34 | dylan.rossi@mailbox.example | Cleveland, OH | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10164 | 2026-06-28 14:58 | nora.perry47@mailbox.example | Buffalo, NY | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | — | — |
| JL-10165 | 2026-06-28 17:11 | noah.turner45@webmail.example | Buffalo, NY | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | RT-20051 | — |
| JL-10166 | 2026-06-28 18:40 | jackson.quinn@inbox.example | San Francisco, CA | Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1; Ceramic Pour-Over Coffee Set ×1 | $106.99 | $0.00 | $106.99 | Visa | Standard | delivered | — | — |
| JL-10167 | 2026-06-28 19:25 | mateo.singh@inbox.example | Austin, TX | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | American Express | Standard | delivered | WC-40016 | — |
| JL-10168 | 2026-06-28 20:22 | mason.gupta52@mailbox.example | Pittsburgh, PA | Smart Plug (2-Pack) ×1; Adjustable Phone Stand ×2; Electric Kettle 1.7L ×1 | $100.00 | $0.00 | $100.00 | Mastercard | Standard | delivered | RT-20023, RF-30051 | — |
| JL-10169 | 2026-06-29 12:04 | maya.patel@inbox.example | San Diego, CA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | American Express | Standard | delivered | — | — |
| JL-10170 | 2026-06-29 14:05 | ingrid.walsh@inbox.example | Buffalo, NY | Ceramic Planter Set ×1; LED Desk Lamp ×1 | $66.50 | $0.00 | $66.50 | Mastercard | Standard | delivered | — | — |
| JL-10171 | 2026-06-29 16:15 | jamal.harris@inbox.example | Louisville, KY | Scented Soy Candle ×3 | $36.00 | $4.99 | $40.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10172 | 2026-06-29 21:32 | isaac.petrov88@mailbox.example | Seattle, WA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | PayPal | Standard | delivered | RT-20041, RF-30070 | — |
| JL-10173 | 2026-06-29 23:51 | wyatt.reyes21@inbox.example | Anchorage, AK | Electric Kettle 1.7L ×2 | $90.00 | $0.00 | $90.00 | PayPal | Standard | delivered | WC-40033 | — |
| JL-10174 | 2026-06-30 07:19 | emma.mitchell@mailbox.example | Austin, TX | Cast Iron Skillet ×1 | $55.00 | $12.99 | $67.99 | Visa | Express | delivered | — | — |
| JL-10175 | 2026-06-30 10:03 | henry.edwards29@inbox.example | Chicago, IL | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10176 | 2026-06-30 12:53 | sophia.gray84@mailbox.example | Baltimore, MD | Ceramic Planter Set ×1; Smart Plug (2-Pack) ×1 | $57.00 | $0.00 | $57.00 | American Express | Standard | delivered | RT-20022, RF-30048 | — |
| JL-11002 | 2026-06-30 18:21 | abigail.thompson55@webmail.example | Los Angeles, CA | Bamboo Cutting Board ×1; Ceramic Planter Set ×1 | $56.00 | $12.99 | $68.99 | Visa | Express | delivered | — | — |
| JL-10178 | 2026-07-01 10:33 | hiro.mitchell@webmail.example | Anchorage, AK | Ceramic Planter Set ×1; Linen Napkins (Set of 4) ×1 | $50.50 | $0.00 | $50.50 | PayPal | Standard | delivered | — | — |
| JL-10179 | 2026-07-01 11:51 | julian.owens85@inbox.example | Des Moines, IA | Bamboo Cutting Board ×1; Scented Soy Candle ×1 | $36.00 | $12.99 | $48.99 | PayPal | Express | delivered | — | — |
| JL-10180 | 2026-07-01 13:42 | maya.lopez39@inbox.example | Honolulu, HI | Wireless Earbuds Pro ×1; Bluetooth Speaker Mini ×1; Scented Soy Candle ×1 | $130.99 | $0.00 | $130.99 | PayPal | Standard | delivered | — | — |
| JL-10181 | 2026-07-01 14:01 | hazel.flores37@inbox.example | Houston, TX | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | — | — |
| JL-10182 | 2026-07-01 14:20 | wyatt.jensen@inbox.example | Washington, DC | Wool Throw Blanket ×1; Adjustable Phone Stand ×2 | $98.00 | $0.00 | $98.00 | Mastercard | Standard | delivered | — | — |
| JL-10183 | 2026-07-01 20:33 | rachel.campbell80@inbox.example | Buffalo, NY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | American Express | Standard | delivered | — | — |
| JL-10184 | 2026-07-01 21:51 | priya.harris@mailbox.example | Anchorage, AK | Linen Napkins (Set of 4) ×2 | $37.00 | $12.99 | $49.99 | PayPal | Express | delivered | — | — |
| JL-10185 | 2026-07-02 00:47 | rachel.hammond@mailbox.example | Albuquerque, NM | Wool Throw Blanket ×2; Linen Napkins (Set of 4) ×1 | $154.50 | $0.00 | $154.50 | American Express | Standard | delivered | RT-20017, RF-30043 | — |
| JL-10186 | 2026-07-02 07:55 | jackson.nelson@webmail.example | Phoenix, AZ | Cast Iron Skillet ×1; Adjustable Phone Stand ×1; Bamboo Cutting Board ×1 | $94.00 | $0.00 | $94.00 | Mastercard | Standard | delivered | — | — |
| JL-10187 | 2026-07-02 10:53 | abigail.davis66@inbox.example | Des Moines, IA | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | — | — |
| JL-10188 | 2026-07-02 11:38 | jackson.anderson55@webmail.example | Denver, CO | LED Desk Lamp ×3; Scented Soy Candle ×2; Wool Throw Blanket ×1; Smart Plug (2-Pack) ×1 | $220.50 | $0.00 | $220.50 | Visa | Standard | delivered | — | — |
| JL-11003 | 2026-07-02 13:11 | amelia.jackson6@webmail.example | Nashville, TN | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10190 | 2026-07-02 14:25 | jamal.harris@inbox.example | Louisville, KY | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | RT-20020, RF-30037 | — |
| JL-10191 | 2026-07-02 15:03 | dylan.nguyen55@inbox.example | Austin, TX | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | WC-40028 | — |
| JL-10192 | 2026-07-02 18:21 | levi.gupta61@webmail.example | Baltimore, MD | Smart Plug (2-Pack) ×1; Oak Side Table ×1; Cast Iron Skillet ×1 | $209.00 | $0.00 | $209.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10193 | 2026-07-03 09:26 | devon.fischer79@webmail.example | Washington, DC | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | PayPal | Standard | delivered | — | — |
| JL-10194 | 2026-07-03 12:09 | abigail.bishop@mailbox.example | New Orleans, LA | Cast Iron Skillet ×2 | $110.00 | $0.00 | $110.00 | Mastercard | Standard | delivered | — | — |
| JL-10195 | 2026-07-03 15:38 | maya.gupta21@mailbox.example | Orlando, FL | Linen Napkins (Set of 4) ×1; Bamboo Cutting Board ×2; Bluetooth Speaker Mini ×1 | $106.49 | $0.00 | $106.49 | PayPal | Standard | delivered | RT-20079 | — |
| JL-10196 | 2026-07-03 16:07 | james.petrov@inbox.example | New Orleans, LA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10197 | 2026-07-03 21:42 | aaliyah.chen85@inbox.example | New York, NY | Personalised Leather Notebook ×1 (emboss "Mom") | $29.00 | $4.99 | $33.99 | Mastercard | Standard | delivered | — | — |
| JL-11004 | 2026-07-03 22:32 | diego.hughes@webmail.example | Cleveland, OH | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | PayPal | Express | delivered | — | — |
| JL-10199 | 2026-07-04 08:19 | priya.jensen@webmail.example | Cleveland, OH | LED Desk Lamp ×1; Personalised Leather Notebook ×2 (emboss "Ben's Notes") | $92.50 | $0.00 | $92.50 | Mastercard | Standard | delivered | WC-40036 | — |
| JL-10200 | 2026-07-04 08:41 | gabriel.foster60@inbox.example | Des Moines, IA | Adjustable Phone Stand ×2 | $30.00 | $4.99 | $34.99 | Visa | Standard | delivered | — | — |
| JL-11005 | 2026-07-04 10:39 | lily.jackson48@mailbox.example | Atlanta, GA | Bamboo Cutting Board ×1; Wireless Earbuds Pro ×1; Ceramic Pour-Over Coffee Set ×1 | $145.00 | $0.00 | $145.00 | Visa | Standard | delivered | RT-20033, RF-30055 | — |
| JL-10202 | 2026-07-04 16:22 | devon.fischer79@webmail.example | Washington, DC | Smart Plug (2-Pack) ×1; Personalised Leather Notebook ×1 (emboss "Thank you, Ms. P") | $54.00 | $0.00 | $54.00 | PayPal | Standard | delivered | RT-20037, RF-30063 | — |
| JL-10203 | 2026-07-04 17:23 | isaac.vasquez@mailbox.example | San Diego, CA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10204 | 2026-07-04 21:48 | arjun.kim63@inbox.example | Detroit, MI | Adjustable Phone Stand ×1; Scented Soy Candle ×2 | $39.00 | $4.99 | $43.99 | Visa | Standard | delivered | — | — |
| JL-11006 | 2026-07-05 07:10 | ethan.anderson@mailbox.example | Las Vegas, NV | Cast Iron Skillet ×2 | $110.00 | $0.00 | $110.00 | PayPal | Standard | delivered | — | — |
| JL-10206 | 2026-07-05 13:14 | hazel.hughes26@mailbox.example | Miami, FL | Smart Plug (2-Pack) ×1 | $25.00 | $12.99 | $37.99 | Mastercard | Express | delivered | — | — |
| JL-10207 | 2026-07-05 13:38 | mason.gupta52@mailbox.example | Pittsburgh, PA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | WC-40007 | — |
| JL-10208 | 2026-07-05 20:59 | aaliyah.edwards@inbox.example | Indianapolis, IN | Personalised Leather Notebook ×3 (emboss "For Maya"); Smart Plug (2-Pack) ×2 | $137.00 | $0.00 | $137.00 | Mastercard | Standard | delivered | RT-20045, RF-30064 | — |
| JL-10209 | 2026-07-05 21:20 | noah.daniels3@mailbox.example | Chicago, IL | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | — | — |
| JL-10210 | 2026-07-05 23:42 | soren.owens@inbox.example | Portland, ME | Scented Soy Candle ×3; Smart Plug (2-Pack) ×2; Bluetooth Speaker Mini ×1 | $125.99 | $0.00 | $125.99 | Visa | Standard | delivered | — | — |
| JL-10211 | 2026-07-06 10:45 | soren.alvarez@inbox.example | Louisville, KY | Ceramic Pour-Over Coffee Set ×1; Wireless Earbuds Pro ×1; Wool Throw Blanket ×1; Cast Iron Skillet ×1 | $244.00 | $0.00 | $244.00 | Visa | Standard | cancelled | RF-30015 | Cancelled 2026-07-06 10:55: Customer request — changed mind |
| JL-11007 | 2026-07-06 12:01 | jamal.kim50@mailbox.example | Portland, OR | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | — | — |
| JL-10213 | 2026-07-06 14:08 | mateo.perry@mailbox.example | Milwaukee, WI | LED Desk Lamp ×1 | $34.50 | $12.99 | $47.49 | Visa | Express | delivered | — | — |
| JL-10214 | 2026-07-06 18:00 | abigail.morgan86@webmail.example | Los Angeles, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | cancelled | RF-30017 | Cancelled 2026-07-07 05:31: Customer request — duplicate order |
| JL-10215 | 2026-07-06 18:36 | fatima.anderson@mailbox.example | Baltimore, MD | Bamboo Cutting Board ×2; Ceramic Planter Set ×1 | $80.00 | $0.00 | $80.00 | Mastercard | Standard | cancelled | RF-30018 | Cancelled 2026-07-07 02:51: Customer request — ordered wrong item |
| JL-10216 | 2026-07-06 18:44 | liam.davis@mailbox.example | Las Vegas, NV | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10217 | 2026-07-06 19:48 | owen.morgan@inbox.example | Charlotte, NC | Bluetooth Speaker Mini ×1; Electric Kettle 1.7L ×1; Cast Iron Skillet ×1 | $139.99 | $0.00 | $139.99 | PayPal | Standard | delivered | RT-20038, RF-30060 | — |
| JL-10218 | 2026-07-07 08:42 | isabella.foster13@inbox.example | Houston, TX | Cast Iron Skillet ×2; Wool Throw Blanket ×1 | $178.00 | $12.99 | $190.99 | PayPal | Express | delivered | — | — |
| JL-11008 | 2026-07-07 10:08 | nora.reyes7@mailbox.example | New York, NY | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10220 | 2026-07-07 11:18 | liam.bennett@webmail.example | Oklahoma City, OK | Bluetooth Speaker Mini ×2; Bamboo Cutting Board ×1 | $103.98 | $12.99 | $116.97 | PayPal | Express | delivered | — | — |
| JL-10221 | 2026-07-07 14:37 | wyatt.jensen@inbox.example | Washington, DC | Cast Iron Skillet ×1; Electric Kettle 1.7L ×1 | $100.00 | $0.00 | $100.00 | PayPal | Standard | delivered | RT-20030, RF-30045 | — |
| JL-10222 | 2026-07-07 16:26 | priya.garcia45@webmail.example | Cleveland, OH | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10223 | 2026-07-07 19:48 | jamal.reyes55@inbox.example | Cleveland, OH | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | RF-30033, INV-50006 | — |
| JL-10224 | 2026-07-08 11:02 | harper.morgan30@webmail.example | Chicago, IL | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | delivered | — | — |
| JL-10225 | 2026-07-08 14:55 | priya.harris@mailbox.example | Anchorage, AK | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Mastercard | Standard | delivered | — | — |
| JL-10226 | 2026-07-08 17:06 | lily.ingram@inbox.example | Oklahoma City, OK | Ceramic Planter Set ×1; Smart Plug (2-Pack) ×1 | $57.00 | $12.99 | $69.99 | Visa | Express | delivered | RT-20081 | — |
| JL-10227 | 2026-07-08 21:49 | rachel.quinn@inbox.example | Denver, CO | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | PayPal | Standard | delivered | — | — |
| JL-11009 | 2026-07-09 09:31 | julian.johnson44@webmail.example | Nashville, TN | LED Desk Lamp ×1; Ceramic Planter Set ×2 | $98.50 | $12.99 | $111.49 | PayPal | Express | delivered | RT-20034, RF-30049 | — |
| JL-10229 | 2026-07-09 10:58 | abigail.hughes@mailbox.example | Orlando, FL | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-11010 | 2026-07-09 12:28 | ava.ellis@mailbox.example | Portland, OR | Ceramic Planter Set ×2 | $64.00 | $0.00 | $64.00 | Visa | Standard | delivered | — | — |
| JL-11011 | 2026-07-09 17:03 | ethan.brooks@webmail.example | Denver, CO | Wireless Earbuds Pro ×1; Bluetooth Speaker Mini ×1 | $118.99 | $0.00 | $118.99 | PayPal | Standard | delivered | — | — |
| JL-10232 | 2026-07-09 17:27 | ava.thompson46@mailbox.example | Honolulu, HI | Linen Napkins (Set of 4) ×1; Oak Side Table ×1 | $147.50 | $12.99 | $160.49 | Mastercard | Express | delivered | — | — |
| JL-11012 | 2026-07-09 19:31 | lucia.petrov51@mailbox.example | Washington, DC | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Visa | Express | delivered | RT-20032, RF-30052 | Delivered after estimated window |
| JL-10234 | 2026-07-10 10:45 | mason.chen@mailbox.example | Richmond, VA | Wool Throw Blanket ×1; Ceramic Planter Set ×1 | $100.00 | $0.00 | $100.00 | Mastercard | Standard | delivered | — | — |
| JL-10235 | 2026-07-10 12:05 | ingrid.nelson@mailbox.example | New York, NY | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10236 | 2026-07-10 13:41 | mei.anderson@mailbox.example | Des Moines, IA | Cast Iron Skillet ×3 | $165.00 | $12.99 | $177.99 | Visa | Express | delivered | RT-20021, RF-30047 | — |
| JL-10237 | 2026-07-10 15:37 | scarlett.thompson@mailbox.example | Omaha, NE | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | PayPal | Standard | delivered | — | — |
| JL-11013 | 2026-07-10 17:22 | ella.harris81@webmail.example | San Francisco, CA | LED Desk Lamp ×2; Wireless Earbuds Pro ×1; Electric Kettle 1.7L ×1; Bluetooth Speaker Mini ×2 | $272.98 | $0.00 | $272.98 | Mastercard | Standard | delivered | RF-30100, WC-40010 | — |
| JL-10239 | 2026-07-10 20:21 | wyatt.patel27@webmail.example | Anchorage, AK | Bluetooth Speaker Mini ×2; Wool Throw Blanket ×1; Wireless Earbuds Pro ×1; Bamboo Cutting Board ×1 | $250.98 | $0.00 | $250.98 | Juniper Lane gift card | Standard | delivered | RT-20024, RF-30046 | — |
| JL-11014 | 2026-07-10 20:41 | julian.ramirez7@webmail.example | Baltimore, MD | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | RT-20061, RF-30085 | Delivered after estimated window |
| JL-10241 | 2026-07-11 10:24 | ava.hammond@mailbox.example | Portland, OR | Adjustable Phone Stand ×2 | $30.00 | $12.99 | $42.99 | Visa | Express | delivered | RT-20055 | — |
| JL-11015 | 2026-07-11 11:31 | owen.ramirez@webmail.example | Boston, MA | Scented Soy Candle ×1; Linen Napkins (Set of 4) ×1 | $30.50 | $4.99 | $35.49 | American Express | Standard | lost | INV-50008 | — |
| JL-10243 | 2026-07-11 14:21 | emma.ingram97@mailbox.example | Charlotte, NC | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Juniper Lane gift card | Standard | lost | RF-30039, INV-50007 | — |
| JL-11016 | 2026-07-11 15:48 | sophia.larson@webmail.example | Denver, CO | Bluetooth Speaker Mini ×1; Oak Side Table ×1; Smart Plug (2-Pack) ×1; Scented Soy Candle ×2 | $217.99 | $12.99 | $230.98 | Visa | Express | delivered | RT-20028, RF-30056 | — |
| JL-10245 | 2026-07-11 15:52 | aaliyah.ortiz@webmail.example | Los Angeles, CA | Wool Throw Blanket ×1; Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1 | $132.99 | $0.00 | $132.99 | Visa | Standard | delivered | — | — |
| JL-10246 | 2026-07-11 19:17 | evelyn.gray92@mailbox.example | Charlotte, NC | Wireless Earbuds Pro ×1; Wool Throw Blanket ×1 | $147.00 | $0.00 | $147.00 | Mastercard | Standard | cancelled | RF-30021 | Cancelled 2026-07-12 07:15: Customer request — duplicate order |
| JL-10247 | 2026-07-12 06:16 | brandon.hammond23@mailbox.example | Austin, TX | Smart Plug (2-Pack) ×1; LED Desk Lamp ×1 | $59.50 | $0.00 | $59.50 | Mastercard | Standard | delivered | — | — |
| JL-10248 | 2026-07-12 09:42 | priya.petrov89@inbox.example | Omaha, NE | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Mastercard | Standard | delivered | — | — |
| JL-10249 | 2026-07-13 01:01 | hiro.chen@inbox.example | Detroit, MI | Adjustable Phone Stand ×1; Bamboo Cutting Board ×1 | $39.00 | $12.99 | $51.99 | Visa | Express | delivered | RT-20042, RF-30065 | — |
| JL-10250 | 2026-07-13 10:03 | olivia.ellis13@inbox.example | Charlotte, NC | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | — | — |
| JL-10251 | 2026-07-13 10:45 | dylan.reyes91@inbox.example | Oklahoma City, OK | Scented Soy Candle ×1; Bluetooth Speaker Mini ×1 | $51.99 | $0.00 | $51.99 | Mastercard | Standard | delivered | — | — |
| JL-10252 | 2026-07-13 13:08 | james.lopez@mailbox.example | Portland, ME | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | RT-20067 | — |
| JL-10253 | 2026-07-13 18:16 | aaliyah.sanders@webmail.example | Kansas City, MO | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10254 | 2026-07-13 20:51 | mei.walker52@webmail.example | Richmond, VA | Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1; Wireless Earbuds Pro ×2; Personalised Leather Notebook ×1 (emboss "Dr. Okafor") | $251.99 | $0.00 | $251.99 | Visa | Standard | delivered | — | — |
| JL-10255 | 2026-07-14 12:01 | fatima.anderson26@mailbox.example | Los Angeles, CA | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | — | — |
| JL-10256 | 2026-07-14 15:47 | evelyn.campbell77@mailbox.example | Honolulu, HI | Bluetooth Speaker Mini ×1; Linen Napkins (Set of 4) ×1; Personalised Leather Notebook ×1 (emboss "For Maya") | $87.49 | $0.00 | $87.49 | Visa | Standard | delivered | WC-40073 | — |
| JL-10257 | 2026-07-14 15:53 | nathan.yamamoto@mailbox.example | Milwaukee, WI | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Juniper Lane gift card | Express | delivered | DMG-55003 | — |
| JL-10258 | 2026-07-14 16:01 | scarlett.bishop@mailbox.example | Detroit, MI | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Juniper Lane gift card | Express | delivered | RT-20039, RF-30071 | — |
| JL-10259 | 2026-07-14 16:54 | tamara.nelson57@inbox.example | Los Angeles, CA | Cast Iron Skillet ×1; Ceramic Planter Set ×1; Scented Soy Candle ×2 | $111.00 | $0.00 | $111.00 | American Express | Standard | delivered | — | — |
| JL-10260 | 2026-07-14 17:50 | harper.reyes17@inbox.example | Orlando, FL | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Visa | Express | delivered | — | — |
| JL-10261 | 2026-07-14 19:20 | evelyn.ingram37@mailbox.example | Portland, ME | Linen Napkins (Set of 4) ×2 | $37.00 | $4.99 | $41.99 | Visa | Standard | delivered | — | — |
| JL-10262 | 2026-07-15 06:37 | soren.owens@inbox.example | Portland, ME | Cast Iron Skillet ×1; LED Desk Lamp ×1; Bluetooth Speaker Mini ×3 | $209.47 | $0.00 | $209.47 | Visa | Standard | delivered | RT-20058, RF-30093 | — |
| JL-10263 | 2026-07-15 08:52 | mia.alvarez@webmail.example | Phoenix, AZ | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | PayPal | Standard | delivered | RT-20040, RF-30072 | — |
| JL-10264 | 2026-07-15 18:19 | isaac.hughes@mailbox.example | Orlando, FL | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | RT-20031 | — |
| JL-10265 | 2026-07-15 18:32 | caleb.vasquez17@webmail.example | Richmond, VA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10266 | 2026-07-15 19:29 | emma.reyes97@mailbox.example | Detroit, MI | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | RT-20048, RF-30073 | — |
| JL-10267 | 2026-07-15 20:20 | sophia.johnson27@mailbox.example | Houston, TX | Scented Soy Candle ×2 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10268 | 2026-07-16 14:36 | aiden.jackson@webmail.example | Houston, TX | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | American Express | Express | cancelled | RF-30023 | Cancelled 2026-07-16 17:25: Customer request — ordered wrong item |
| JL-10269 | 2026-07-16 15:58 | olivia.kelly@inbox.example | Boston, MA | Bluetooth Speaker Mini ×3; Electric Kettle 1.7L ×1 | $164.97 | $0.00 | $164.97 | PayPal | Standard | delivered | RT-20047, RF-30067 | — |
| JL-10270 | 2026-07-16 17:29 | ingrid.kim57@inbox.example | Anchorage, AK | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | RT-20035, RF-30057 | — |
| JL-10271 | 2026-07-16 19:06 | noah.novak70@mailbox.example | Boise, ID | Wireless Earbuds Pro ×1; Wool Throw Blanket ×2; Linen Napkins (Set of 4) ×1 | $233.50 | $0.00 | $233.50 | Visa | Standard | delivered | — | — |
| JL-10272 | 2026-07-17 09:24 | henry.edwards29@inbox.example | Chicago, IL | Personalised Leather Notebook ×1 (emboss "A. Rivera") | $29.00 | $12.99 | $41.99 | Mastercard | Express | delivered | — | — |
| JL-10273 | 2026-07-17 12:40 | owen.morgan@inbox.example | Charlotte, NC | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10274 | 2026-07-17 13:30 | mei.mitchell55@mailbox.example | Atlanta, GA | Personalised Leather Notebook ×1 (emboss "For Maya"); Bluetooth Speaker Mini ×1 | $68.99 | $0.00 | $68.99 | PayPal | Standard | delivered | — | — |
| JL-10275 | 2026-07-17 15:40 | abigail.bishop@mailbox.example | New Orleans, LA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10276 | 2026-07-17 17:25 | harper.reyes17@inbox.example | Orlando, FL | Ceramic Planter Set ×1; Cast Iron Skillet ×1 | $87.00 | $0.00 | $87.00 | PayPal | Standard | delivered | — | — |
| JL-10277 | 2026-07-17 18:58 | tamara.jackson@inbox.example | Los Angeles, CA | Electric Kettle 1.7L ×1; LED Desk Lamp ×2 | $114.00 | $0.00 | $114.00 | Mastercard | Standard | delivered | — | — |
| JL-10278 | 2026-07-17 22:43 | nora.zimmerman72@inbox.example | Boise, ID | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $74.49 | $0.00 | $74.49 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10279 | 2026-07-18 05:26 | aaliyah.anderson@mailbox.example | Tampa, FL | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10280 | 2026-07-18 16:06 | zoey.zimmerman@inbox.example | Richmond, VA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | WC-40039 | — |
| JL-10281 | 2026-07-18 16:10 | chloe.perry@webmail.example | Houston, TX | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | cancelled | RF-30026 | Cancelled 2026-07-19 07:06: Customer request — changed mind |
| JL-10282 | 2026-07-18 17:13 | mason.chen@mailbox.example | Richmond, VA | Adjustable Phone Stand ×1; Electric Kettle 1.7L ×1 | $60.00 | $0.00 | $60.00 | Visa | Standard | delivered | WC-40024 | — |
| JL-10283 | 2026-07-18 17:14 | owen.carter56@mailbox.example | Charlotte, NC | Adjustable Phone Stand ×3; Wireless Earbuds Pro ×2 | $203.00 | $0.00 | $203.00 | Visa | Standard | delivered | — | — |
| JL-10284 | 2026-07-18 18:04 | mateo.perry@mailbox.example | Milwaukee, WI | Personalised Leather Notebook ×1 (emboss "Field Notes - LK"); Scented Soy Candle ×1; Bluetooth Speaker Mini ×1 | $80.99 | $12.99 | $93.98 | Visa | Express | delivered | RT-20063, RF-30086 | Delivered after estimated window |
| JL-10285 | 2026-07-18 18:23 | henry.daniels40@inbox.example | Los Angeles, CA | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Visa | Express | delivered | — | — |
| JL-10286 | 2026-07-18 18:54 | gabriel.chen44@webmail.example | Los Angeles, CA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10287 | 2026-07-18 21:09 | emma.ingram97@mailbox.example | Charlotte, NC | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1; Ceramic Pour-Over Coffee Set ×2; Wireless Earbuds Pro ×1 | $237.49 | $0.00 | $237.49 | Mastercard | Standard | delivered | RT-20046, RF-30068 | — |
| JL-10288 | 2026-07-18 21:13 | ingrid.gray@mailbox.example | Portland, ME | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Mastercard | Standard | delivered | WC-40022 | — |
| JL-10289 | 2026-07-19 01:31 | ingrid.singh@mailbox.example | Houston, TX | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Mastercard | Standard | delivered | — | — |
| JL-10290 | 2026-07-19 12:02 | zoey.ortiz77@mailbox.example | Milwaukee, WI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10291 | 2026-07-19 13:13 | brandon.kim15@webmail.example | Albuquerque, NM | Wireless Earbuds Pro ×1; LED Desk Lamp ×1 | $113.50 | $0.00 | $113.50 | Visa | Standard | cancelled | RF-30027 | Cancelled 2026-07-19 16:01: Customer request — duplicate order |
| JL-10292 | 2026-07-19 14:14 | aaliyah.daniels17@webmail.example | Baltimore, MD | Ceramic Planter Set ×1; LED Desk Lamp ×2 | $101.00 | $0.00 | $101.00 | Visa | Standard | delivered | WC-40054 | — |
| JL-10293 | 2026-07-19 18:18 | lily.reyes25@mailbox.example | Cleveland, OH | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Juniper Lane gift card | Standard | delivered | WC-40065 | — |
| JL-10294 | 2026-07-20 06:54 | levi.underwood39@mailbox.example | Salt Lake City, UT | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10295 | 2026-07-20 07:43 | aaliyah.alvarez34@mailbox.example | Richmond, VA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | RT-20036 | — |
| JL-10296 | 2026-07-20 14:33 | grace.patel@inbox.example | Houston, TX | Wool Throw Blanket ×2; LED Desk Lamp ×1 | $170.50 | $0.00 | $170.50 | PayPal | Standard | delivered | RT-20090 | — |
| JL-10297 | 2026-07-20 20:58 | sophia.gray84@mailbox.example | Baltimore, MD | Wireless Earbuds Pro ×2 | $158.00 | $0.00 | $158.00 | Mastercard | Standard | delivered | RT-20056 | — |
| JL-10298 | 2026-07-20 21:43 | amelia.daniels94@mailbox.example | Detroit, MI | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Mastercard | Express | delivered | — | — |
| JL-10299 | 2026-07-21 10:04 | soren.carter@mailbox.example | Denver, CO | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Mastercard | Express | cancelled | RF-30030 | Cancelled 2026-07-21 15:10: Customer request — changed mind |
| JL-10300 | 2026-07-21 11:02 | jackson.martinez78@mailbox.example | Minneapolis, MN | Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam") | $58.00 | $0.00 | $58.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10301 | 2026-07-21 12:42 | mia.nelson29@webmail.example | San Francisco, CA | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10302 | 2026-07-21 17:38 | jamal.donovan5@mailbox.example | Cleveland, OH | Ceramic Planter Set ×1; Wireless Earbuds Pro ×2 | $190.00 | $0.00 | $190.00 | Visa | Standard | delivered | — | — |
| JL-10303 | 2026-07-21 18:36 | diego.jackson8@webmail.example | Portland, OR | Cast Iron Skillet ×1; Wool Throw Blanket ×1 | $123.00 | $0.00 | $123.00 | Mastercard | Standard | delivered | — | — |
| JL-10304 | 2026-07-21 20:05 | tessa.edwards1@webmail.example | Tampa, FL | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | cancelled | RF-30031 | Cancelled 2026-07-22 04:06: Customer request — changed mind |
| JL-10305 | 2026-07-22 01:54 | fatima.alvarez@mailbox.example | Albuquerque, NM | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | — | — |
| JL-10306 | 2026-07-22 08:23 | chloe.bishop@webmail.example | Charlotte, NC | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Visa | Express | delivered | RF-30213, WC-40057 | — |
| JL-10307 | 2026-07-22 08:41 | caleb.ortiz@inbox.example | Indianapolis, IN | Cast Iron Skillet ×1 | $55.00 | $12.99 | $67.99 | American Express | Express | delivered | — | — |
| JL-10308 | 2026-07-22 09:23 | abigail.jackson62@mailbox.example | Atlanta, GA | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | PayPal | Email (digital) | delivered | RT-20043 | — |
| JL-10309 | 2026-07-22 09:23 | ingrid.anderson40@mailbox.example | Boise, ID | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | PayPal | Standard | cancelled | RF-30032 | Cancelled 2026-07-22 10:58: Customer request — ordered wrong item |
| JL-10310 | 2026-07-22 13:20 | ingrid.gray@mailbox.example | Portland, ME | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | RT-20049, RF-30080 | — |
| JL-10311 | 2026-07-22 15:29 | ethan.kim19@inbox.example | Indianapolis, IN | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Juniper Lane gift card | Standard | delivered | WC-40029 | — |
| JL-10312 | 2026-07-22 17:53 | ethan.turner96@mailbox.example | Louisville, KY | Juniper Lane Gift Card ×2 ($50.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10313 | 2026-07-22 22:20 | harper.okafor37@webmail.example | Salt Lake City, UT | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | RT-20044, RF-30066 | — |
| JL-10314 | 2026-07-23 14:53 | jamal.lewis@inbox.example | Atlanta, GA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10315 | 2026-07-24 05:59 | emma.daniels@inbox.example | New York, NY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10316 | 2026-07-24 18:04 | mei.kim@webmail.example | Las Vegas, NV | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10317 | 2026-07-24 18:38 | keisha.ingram64@inbox.example | New York, NY | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | RT-20095 | — |
| JL-10318 | 2026-07-24 19:20 | gabriel.walsh31@inbox.example | New York, NY | Bamboo Cutting Board ×2 | $48.00 | $4.99 | $52.99 | Visa | Standard | delivered | — | — |
| JL-10319 | 2026-07-24 21:16 | caleb.edwards@webmail.example | Miami, FL | Scented Soy Candle ×1; Electric Kettle 1.7L ×1 | $57.00 | $0.00 | $57.00 | Mastercard | Standard | delivered | — | — |
| JL-10320 | 2026-07-25 10:32 | aiden.jackson@webmail.example | Houston, TX | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | — | — |
| JL-10321 | 2026-07-25 11:44 | dylan.davis@mailbox.example | Kansas City, MO | Ceramic Pour-Over Coffee Set ×1; Wireless Earbuds Pro ×2; Linen Napkins (Set of 4) ×3 | $255.50 | $0.00 | $255.50 | Visa | Standard | delivered | WC-40015 | — |
| JL-10322 | 2026-07-25 12:21 | jamal.gray42@inbox.example | Dallas, TX | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | PayPal | Express | delivered | — | — |
| JL-10323 | 2026-07-25 17:26 | levi.chen@inbox.example | Salt Lake City, UT | Smart Plug (2-Pack) ×1; Wireless Earbuds Pro ×1 | $104.00 | $0.00 | $104.00 | Mastercard | Standard | cancelled | RF-30038 | Cancelled 2026-07-25 19:32: Customer request — duplicate order |
| JL-10324 | 2026-07-26 10:36 | grace.gray9@inbox.example | Baltimore, MD | Electric Kettle 1.7L ×2; Wireless Earbuds Pro ×1 | $169.00 | $0.00 | $169.00 | American Express | Standard | delivered | — | — |
| JL-10325 | 2026-07-26 17:05 | jackson.daniels74@mailbox.example | Miami, FL | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Mastercard | Express | delivered | RT-20074, RF-30094 | — |
| JL-10326 | 2026-07-26 20:23 | caleb.hammond80@webmail.example | Las Vegas, NV | Personalised Leather Notebook ×1 (emboss "Team Lead"); Ceramic Planter Set ×1; Scented Soy Candle ×1 | $73.00 | $0.00 | $73.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10327 | 2026-07-27 08:13 | mason.perry75@webmail.example | Providence, RI | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | WC-40064 | — |
| JL-10328 | 2026-07-27 10:30 | owen.walker@mailbox.example | Kansas City, MO | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | PayPal | Express | delivered | — | — |
| JL-10329 | 2026-07-27 17:21 | zoey.zimmerman@inbox.example | Richmond, VA | Personalised Leather Notebook ×1 (emboss "A. Rivera"); Bamboo Cutting Board ×1 | $53.00 | $0.00 | $53.00 | Mastercard | Standard | delivered | — | — |
| JL-10330 | 2026-07-27 20:48 | mason.bishop5@webmail.example | Milwaukee, WI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | — | — |
| JL-10331 | 2026-07-27 21:24 | priya.owens@mailbox.example | Nashville, TN | Electric Kettle 1.7L ×1; LED Desk Lamp ×1 | $79.50 | $0.00 | $79.50 | Visa | Standard | delivered | RT-20064, RF-30089 | — |
| JL-10332 | 2026-07-28 08:22 | lucas.quinn@mailbox.example | Baltimore, MD | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $12.99 | $54.99 | Visa | Express | delivered | RT-20052, RF-30074 | — |
| JL-10333 | 2026-07-28 09:07 | nathan.gray37@mailbox.example | Buffalo, NY | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | American Express | Standard | delivered | WC-40023 | — |
| JL-10334 | 2026-07-28 11:03 | emma.daniels@inbox.example | New York, NY | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Mastercard | Standard | delivered | WC-40027 | — |
| JL-10335 | 2026-07-28 15:29 | priya.perry@webmail.example | Portland, ME | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10336 | 2026-07-28 16:00 | caleb.lewis@webmail.example | Providence, RI | Scented Soy Candle ×1; Smart Plug (2-Pack) ×1 | $37.00 | $4.99 | $41.99 | American Express | Standard | delivered | — | — |
| JL-10337 | 2026-07-29 03:55 | zoey.gupta@mailbox.example | Raleigh, NC | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10338 | 2026-07-29 12:24 | james.hammond93@webmail.example | Las Vegas, NV | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10339 | 2026-07-29 14:38 | scarlett.patel48@inbox.example | Minneapolis, MN | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | cancelled | RF-30044 | Cancelled 2026-07-30 12:59: Customer request — ordered wrong item |
| JL-10340 | 2026-07-29 15:46 | levi.underwood39@mailbox.example | Salt Lake City, UT | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | Mastercard | Express | delivered | — | — |
| JL-10341 | 2026-07-29 16:09 | levi.edwards27@webmail.example | Buffalo, NY | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | RT-20065 | — |
| JL-10342 | 2026-07-29 17:43 | noah.young82@webmail.example | Honolulu, HI | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10343 | 2026-07-29 18:27 | mason.singh47@mailbox.example | Charlotte, NC | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | RT-20050, RF-30081 | — |
| JL-10344 | 2026-07-29 21:16 | noah.young82@webmail.example | Honolulu, HI | Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×1 | $63.99 | $0.00 | $63.99 | PayPal | Standard | delivered | — | — |
| JL-10345 | 2026-07-30 06:06 | ethan.foster66@mailbox.example | Los Angeles, CA | Cast Iron Skillet ×1; Wireless Earbuds Pro ×1 | $134.00 | $0.00 | $134.00 | Visa | Standard | delivered | RT-20108 | — |
| JL-10346 | 2026-07-30 08:10 | scarlett.garcia45@webmail.example | Seattle, WA | Ceramic Planter Set ×1; Wool Throw Blanket ×1 | $100.00 | $0.00 | $100.00 | PayPal | Standard | delivered | RT-20059, RF-30090 | — |
| JL-10347 | 2026-07-30 11:12 | isaac.martinez95@webmail.example | Philadelphia, PA | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Visa | Standard | delivered | — | — |
| JL-10348 | 2026-07-30 11:52 | lily.turner@webmail.example | Boston, MA | Ceramic Planter Set ×2; Scented Soy Candle ×1 | $76.00 | $0.00 | $76.00 | PayPal | Standard | delivered | — | — |
| JL-10349 | 2026-07-30 15:20 | hiro.ramirez27@inbox.example | Las Vegas, NV | Ceramic Pour-Over Coffee Set ×1; Bamboo Cutting Board ×1 | $66.00 | $0.00 | $66.00 | Visa | Standard | delivered | RT-20054, RF-30082 | — |
| JL-10350 | 2026-07-30 15:52 | maya.davis27@webmail.example | New Orleans, LA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | American Express | Standard | delivered | RT-20066, RF-30087 | — |
| JL-10351 | 2026-07-30 20:41 | keisha.foster@mailbox.example | Baltimore, MD | Adjustable Phone Stand ×1; Electric Kettle 1.7L ×1; Personalised Leather Notebook ×2 (emboss "Dad") | $118.00 | $0.00 | $118.00 | Mastercard | Standard | delivered | — | — |
| JL-10352 | 2026-07-31 03:18 | zoey.ellis36@webmail.example | Providence, RI | Electric Kettle 1.7L ×1; Wool Throw Blanket ×1 | $113.00 | $0.00 | $113.00 | Mastercard | Standard | delivered | — | — |
| JL-10353 | 2026-07-31 06:27 | lucas.owens@webmail.example | Washington, DC | Wool Throw Blanket ×1; Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "J\&M 2026") | $109.00 | $12.99 | $121.99 | Visa | Express | delivered | — | — |
| JL-10354 | 2026-07-31 08:25 | chloe.chen@inbox.example | New Orleans, LA | Adjustable Phone Stand ×2 | $30.00 | $4.99 | $34.99 | Mastercard | Standard | delivered | — | Delivered after estimated window |
| JL-10355 | 2026-07-31 08:40 | aaliyah.carter@inbox.example | Minneapolis, MN | Wireless Earbuds Pro ×3; Cast Iron Skillet ×2; Ceramic Pour-Over Coffee Set ×1 | $389.00 | $0.00 | $389.00 | Mastercard | Standard | delivered | — | — |
| JL-10356 | 2026-07-31 12:55 | mateo.larson@inbox.example | San Diego, CA | Scented Soy Candle ×1; Oak Side Table ×1; LED Desk Lamp ×2; Cast Iron Skillet ×1 | $265.00 | $12.99 | $277.99 | PayPal | Express | delivered | — | — |
| JL-10357 | 2026-07-31 15:06 | grace.walker@mailbox.example | Burlington, VT | LED Desk Lamp ×1; Bamboo Cutting Board ×1 | $58.50 | $12.99 | $71.49 | Visa | Express | delivered | — | — |
| JL-10358 | 2026-07-31 18:14 | isaac.garcia72@inbox.example | Richmond, VA | Oak Side Table ×1; Electric Kettle 1.7L ×1 | $174.00 | $0.00 | $174.00 | PayPal | Standard | delivered | INV-50009 | — |
| JL-10359 | 2026-08-01 11:05 | aiden.kelly@webmail.example | San Francisco, CA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10360 | 2026-08-01 12:27 | mateo.young@webmail.example | Raleigh, NC | Cast Iron Skillet ×1; Bamboo Cutting Board ×3; Linen Napkins (Set of 4) ×2 | $164.00 | $0.00 | $164.00 | Mastercard | Standard | delivered | — | — |
| JL-10361 | 2026-08-01 12:57 | lucia.campbell@mailbox.example | New York, NY | Bluetooth Speaker Mini ×1; Scented Soy Candle ×1 | $51.99 | $0.00 | $51.99 | Visa | Standard | delivered | INV-50010 | — |
| JL-10362 | 2026-08-01 13:44 | zoey.underwood@webmail.example | Oklahoma City, OK | Juniper Lane Gift Card ×2 ($50.00 card) | $100.00 | $0.00 | $100.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10363 | 2026-08-01 18:53 | priya.ingram18@inbox.example | San Francisco, CA | Scented Soy Candle ×2; Electric Kettle 1.7L ×1; Wool Throw Blanket ×2 | $205.00 | $0.00 | $205.00 | PayPal | Standard | delivered | WC-40047 | Delivered after estimated window |
| JL-10364 | 2026-08-02 10:01 | elijah.gupta@webmail.example | Denver, CO | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | — | — |
| JL-10365 | 2026-08-02 11:05 | tamara.bishop@webmail.example | Des Moines, IA | Cast Iron Skillet ×1; Scented Soy Candle ×1; LED Desk Lamp ×1 | $101.50 | $0.00 | $101.50 | PayPal | Standard | delivered | RT-20075, RF-30108 | — |
| JL-10366 | 2026-08-02 12:40 | jamal.thompson70@mailbox.example | Indianapolis, IN | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | RT-20053, RF-30083 | — |
| JL-10367 | 2026-08-02 12:43 | ethan.kelly@inbox.example | Los Angeles, CA | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10368 | 2026-08-02 13:12 | owen.nguyen@mailbox.example | Richmond, VA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | WC-40021 | — |
| JL-10369 | 2026-08-02 13:31 | scarlett.ingram4@inbox.example | Des Moines, IA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10370 | 2026-08-02 18:15 | sophia.patel@webmail.example | Denver, CO | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | PayPal | Standard | delivered | RF-30061, DMG-55004 | — |
| JL-10371 | 2026-08-02 19:49 | diego.thompson@mailbox.example | San Francisco, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10372 | 2026-08-02 20:53 | noah.turner45@webmail.example | Buffalo, NY | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | RT-20060 | — |
| JL-10373 | 2026-08-04 02:28 | isabella.vasquez43@mailbox.example | Seattle, WA | Linen Napkins (Set of 4) ×1; Scented Soy Candle ×1 | $30.50 | $4.99 | $35.49 | Mastercard | Standard | delivered | RT-20085, RF-30109 | — |
| JL-10374 | 2026-08-04 05:16 | tessa.sanders83@inbox.example | Charlotte, NC | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | PayPal | Standard | delivered | — | — |
| JL-10375 | 2026-08-04 06:59 | ava.hammond@mailbox.example | Portland, OR | Scented Soy Candle ×1; Electric Kettle 1.7L ×2 | $102.00 | $0.00 | $102.00 | Mastercard | Standard | delivered | RT-20057, RF-30095 | — |
| JL-10376 | 2026-08-04 11:34 | brandon.hammond23@mailbox.example | Austin, TX | Ceramic Pour-Over Coffee Set ×1; Bluetooth Speaker Mini ×3; Oak Side Table ×1 | $290.97 | $0.00 | $290.97 | Visa | Standard | delivered | RT-20105 | — |
| JL-10377 | 2026-08-04 16:40 | lucia.larson@webmail.example | Washington, DC | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | RT-20062, RF-30091 | — |
| JL-10378 | 2026-08-05 06:51 | maya.campbell@inbox.example | Honolulu, HI | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | Mastercard | Standard | delivered | — | — |
| JL-10379 | 2026-08-05 10:59 | james.chen59@webmail.example | Detroit, MI | Scented Soy Candle ×1; LED Desk Lamp ×1 | $46.50 | $4.99 | $51.49 | Visa | Standard | delivered | RT-20072, RF-30096 | — |
| JL-10380 | 2026-08-05 13:10 | ava.davis@mailbox.example | San Francisco, CA | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | PayPal | Standard | delivered | — | — |
| JL-10381 | 2026-08-05 15:05 | henry.lewis@mailbox.example | Salt Lake City, UT | Ceramic Pour-Over Coffee Set ×1; Smart Plug (2-Pack) ×1 | $67.00 | $12.99 | $79.99 | PayPal | Express | delivered | WC-40025 | — |
| JL-10382 | 2026-08-05 18:26 | lily.fischer@webmail.example | Chicago, IL | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | cancelled | RF-30053 | Cancelled 2026-08-06 00:18: Customer request — ordered wrong item |
| JL-10383 | 2026-08-05 20:01 | keisha.martinez9@mailbox.example | Las Vegas, NV | Wireless Earbuds Pro ×3; Personalised Leather Notebook ×2 (emboss "Team Lead") | $295.00 | $0.00 | $295.00 | Mastercard | Standard | delivered | — | — |
| JL-10384 | 2026-08-05 21:05 | grace.young75@inbox.example | Burlington, VT | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | — | — |
| JL-10385 | 2026-08-05 21:15 | logan.turner@webmail.example | Atlanta, GA | Bluetooth Speaker Mini ×1; Ceramic Pour-Over Coffee Set ×3 | $165.99 | $0.00 | $165.99 | Mastercard | Standard | cancelled | RF-30054 | Cancelled 2026-08-06 10:54: Customer request — found item elsewhere |
| JL-10386 | 2026-08-05 21:54 | elijah.jackson12@webmail.example | New York, NY | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $74.49 | $0.00 | $74.49 | American Express | Standard | delivered | — | — |
| JL-10387 | 2026-08-06 08:28 | caleb.ortiz@inbox.example | Indianapolis, IN | Cast Iron Skillet ×1; Linen Napkins (Set of 4) ×1; Bamboo Cutting Board ×1 | $97.50 | $0.00 | $97.50 | Mastercard | Standard | delivered | — | — |
| JL-10388 | 2026-08-06 09:06 | chloe.okafor@inbox.example | Charlotte, NC | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10389 | 2026-08-06 11:31 | caleb.hammond80@webmail.example | Las Vegas, NV | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | — | — |
| JL-10390 | 2026-08-06 21:42 | diego.daniels49@mailbox.example | Indianapolis, IN | Bluetooth Speaker Mini ×2 | $79.98 | $0.00 | $79.98 | Visa | Standard | delivered | RT-20123 | — |
| JL-10391 | 2026-08-07 08:44 | zoey.zimmerman@inbox.example | Richmond, VA | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Mastercard | Standard | delivered | RT-20070, RF-30098 | Delivered after estimated window |
| JL-10392 | 2026-08-07 09:40 | ella.thompson@mailbox.example | Omaha, NE | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | INV-50011 | — |
| JL-10393 | 2026-08-07 15:42 | rachel.daniels91@mailbox.example | San Francisco, CA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Juniper Lane gift card | Standard | lost | INV-50012 | — |
| JL-10394 | 2026-08-07 17:26 | elijah.ingram@webmail.example | Cleveland, OH | Scented Soy Candle ×1; Electric Kettle 1.7L ×1 | $57.00 | $0.00 | $57.00 | Visa | Standard | cancelled | RF-30058 | Cancelled 2026-08-08 01:43: Customer request — found item elsewhere |
| JL-10395 | 2026-08-07 20:34 | elijah.daniels@inbox.example | Buffalo, NY | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | lost | RF-30078, INV-50013 | — |
| JL-10396 | 2026-08-08 11:49 | hazel.hughes26@mailbox.example | Miami, FL | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | RT-20068, RF-30092 | — |
| JL-10397 | 2026-08-08 14:08 | ella.harris81@webmail.example | San Francisco, CA | Cast Iron Skillet ×1; Ceramic Planter Set ×1 | $87.00 | $0.00 | $87.00 | American Express | Standard | delivered | — | — |
| JL-10398 | 2026-08-08 16:30 | omar.daniels73@mailbox.example | Los Angeles, CA | Smart Plug (2-Pack) ×2; Wireless Earbuds Pro ×1; Adjustable Phone Stand ×1 | $144.00 | $0.00 | $144.00 | Mastercard | Standard | delivered | RT-20089, RF-30115 | — |
| JL-10399 | 2026-08-08 23:06 | evelyn.sanders96@mailbox.example | Portland, OR | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | PayPal | Standard | delivered | RT-20080, RF-30110 | — |
| JL-10400 | 2026-08-09 09:39 | marcus.yamamoto36@mailbox.example | Phoenix, AZ | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | American Express | Express | delivered | — | — |
| JL-10401 | 2026-08-09 11:19 | lily.underwood@inbox.example | Baltimore, MD | Oak Side Table ×1; Bluetooth Speaker Mini ×2; Scented Soy Candle ×1 | $220.98 | $12.99 | $233.97 | Visa | Express | lost | RF-30079, INV-50014 | — |
| JL-10402 | 2026-08-09 11:27 | brandon.jackson85@webmail.example | San Francisco, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | American Express | Standard | delivered | — | — |
| JL-10403 | 2026-08-09 12:44 | tamara.ingram80@inbox.example | Atlanta, GA | Electric Kettle 1.7L ×1; Linen Napkins (Set of 4) ×2 | $82.00 | $0.00 | $82.00 | Mastercard | Standard | delivered | WC-40030 | — |
| JL-10404 | 2026-08-09 13:14 | marcus.patel81@webmail.example | Burlington, VT | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | PayPal | Express | delivered | RT-20071, RF-30103 | — |
| JL-10405 | 2026-08-09 16:14 | liam.jensen@webmail.example | Seattle, WA | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | — | — |
| JL-10406 | 2026-08-09 18:39 | chloe.zimmerman@mailbox.example | Baltimore, MD | Adjustable Phone Stand ×1; Linen Napkins (Set of 4) ×1 | $33.50 | $12.99 | $46.49 | Juniper Lane gift card | Express | delivered | — | — |
| JL-10407 | 2026-08-10 07:02 | scarlett.young@inbox.example | Boston, MA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | RT-20077, RF-30111 | — |
| JL-10408 | 2026-08-10 17:50 | hazel.hughes26@mailbox.example | Miami, FL | Bamboo Cutting Board ×1; Adjustable Phone Stand ×1 | $39.00 | $4.99 | $43.99 | Visa | Standard | delivered | — | — |
| JL-10409 | 2026-08-10 19:05 | nathan.fischer80@webmail.example | Minneapolis, MN | Electric Kettle 1.7L ×2; Linen Napkins (Set of 4) ×1 | $108.50 | $0.00 | $108.50 | Visa | Standard | delivered | RT-20120 | — |
| JL-10410 | 2026-08-11 09:41 | rachel.nguyen@mailbox.example | Atlanta, GA | Smart Plug (2-Pack) ×1; Bamboo Cutting Board ×1 | $49.00 | $4.99 | $53.99 | Visa | Standard | delivered | — | — |
| JL-10411 | 2026-08-11 10:06 | evelyn.hughes@mailbox.example | Raleigh, NC | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Mastercard | Standard | delivered | — | — |
| JL-10412 | 2026-08-11 11:20 | gabriel.rossi52@inbox.example | Seattle, WA | Electric Kettle 1.7L ×1; Adjustable Phone Stand ×1; Scented Soy Candle ×1 | $72.00 | $0.00 | $72.00 | PayPal | Standard | delivered | — | — |
| JL-10413 | 2026-08-11 15:08 | ethan.anderson44@inbox.example | Los Angeles, CA | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | DMG-55005 | — |
| JL-10414 | 2026-08-11 15:17 | gabriel.zimmerman69@inbox.example | Louisville, KY | Electric Kettle 1.7L ×1; Bluetooth Speaker Mini ×1 | $84.99 | $0.00 | $84.99 | Visa | Standard | delivered | — | — |
| JL-10415 | 2026-08-12 04:27 | lily.thompson30@mailbox.example | New York, NY | Bamboo Cutting Board ×1; Wireless Earbuds Pro ×1 | $103.00 | $0.00 | $103.00 | PayPal | Standard | delivered | — | — |
| JL-10416 | 2026-08-12 09:04 | chloe.sanders88@webmail.example | Des Moines, IA | Smart Plug (2-Pack) ×2; LED Desk Lamp ×1; Adjustable Phone Stand ×1 | $99.50 | $0.00 | $99.50 | Mastercard | Standard | delivered | — | — |
| JL-10417 | 2026-08-13 06:04 | arjun.rossi@inbox.example | Honolulu, HI | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | delivered | RT-20069, RF-30097 | — |
| JL-10418 | 2026-08-13 07:18 | zoey.ortiz77@mailbox.example | Milwaukee, WI | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | American Express | Standard | delivered | — | — |
| JL-10419 | 2026-08-13 09:29 | maya.davis27@mailbox.example | Houston, TX | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | RT-20121 | — |
| JL-10420 | 2026-08-13 13:56 | owen.sanders@mailbox.example | Portland, ME | Scented Soy Candle ×1; Electric Kettle 1.7L ×1 | $57.00 | $0.00 | $57.00 | Visa | Standard | delivered | RT-20092, RF-30119 | — |
| JL-10421 | 2026-08-13 18:54 | maya.gray@webmail.example | New Orleans, LA | Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×2 | $103.98 | $0.00 | $103.98 | Mastercard | Standard | delivered | — | — |
| JL-10422 | 2026-08-14 09:54 | nora.hughes@inbox.example | Minneapolis, MN | Ceramic Pour-Over Coffee Set ×1; Scented Soy Candle ×1; Personalised Leather Notebook ×2 (emboss "Team Lead") | $112.00 | $0.00 | $112.00 | Mastercard | Standard | delivered | — | — |
| JL-10423 | 2026-08-14 09:55 | aria.young@mailbox.example | Orlando, FL | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10424 | 2026-08-14 12:46 | ava.turner67@webmail.example | Salt Lake City, UT | Ceramic Pour-Over Coffee Set ×1; Bluetooth Speaker Mini ×1 | $81.99 | $0.00 | $81.99 | American Express | Standard | delivered | — | — |
| JL-10425 | 2026-08-14 13:57 | aaliyah.gray72@webmail.example | Des Moines, IA | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | Mastercard | Standard | delivered | — | — |
| JL-10426 | 2026-08-14 15:58 | scarlett.young@inbox.example | Boston, MA | Cast Iron Skillet ×1; Bamboo Cutting Board ×2; Ceramic Pour-Over Coffee Set ×1; Scented Soy Candle ×2 | $169.00 | $0.00 | $169.00 | PayPal | Standard | delivered | RT-20102, RF-30129 | — |
| JL-10427 | 2026-08-14 17:20 | amelia.larson93@webmail.example | San Francisco, CA | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | PayPal | Standard | delivered | — | — |
| JL-10428 | 2026-08-14 17:37 | amelia.sanders@mailbox.example | Dallas, TX | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | American Express | Email (digital) | delivered | — | — |
| JL-10429 | 2026-08-14 21:14 | lucia.okafor@mailbox.example | Kansas City, MO | Oak Side Table ×1 | $129.00 | $12.99 | $141.99 | American Express | Express | delivered | — | — |
| JL-10430 | 2026-08-14 21:20 | hiro.harris50@mailbox.example | Tampa, FL | Adjustable Phone Stand ×1; Wireless Earbuds Pro ×1 | $94.00 | $12.99 | $106.99 | Mastercard | Express | delivered | — | — |
| JL-10431 | 2026-08-15 10:53 | abigail.ellis51@webmail.example | Richmond, VA | Adjustable Phone Stand ×16 | $240.00 | $0.00 | $240.00 | Visa | Standard | cancelled | RF-30062 | Cancelled 2026-08-16 00:17: More than 10 units of one product; stock limited — support contacted customer first |
| JL-10432 | 2026-08-15 11:02 | mei.owens56@mailbox.example | San Diego, CA | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | PayPal | Express | delivered | — | — |
| JL-10433 | 2026-08-15 21:26 | jamal.lopez@mailbox.example | Des Moines, IA | Cast Iron Skillet ×1; Scented Soy Candle ×1; Bamboo Cutting Board ×1 | $91.00 | $0.00 | $91.00 | Mastercard | Standard | delivered | RT-20097, RF-30130 | — |
| JL-10434 | 2026-08-16 00:37 | aria.reyes94@webmail.example | Raleigh, NC | Adjustable Phone Stand ×3 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10435 | 2026-08-16 06:16 | jamal.kim50@mailbox.example | Portland, OR | Scented Soy Candle ×2; Personalised Leather Notebook ×1 (emboss "Thank you, Ms. P") | $53.00 | $0.00 | $53.00 | Mastercard | Standard | delivered | RT-20109, RF-30141 | — |
| JL-10436 | 2026-08-16 07:03 | lucas.daniels3@webmail.example | Boise, ID | LED Desk Lamp ×1; Bluetooth Speaker Mini ×2; Electric Kettle 1.7L ×2 | $204.48 | $0.00 | $204.48 | PayPal | Standard | delivered | RT-20076, RF-30107 | — |
| JL-10437 | 2026-08-16 07:55 | jamal.garcia@webmail.example | Oklahoma City, OK | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | — | — |
| JL-10438 | 2026-08-16 11:57 | liam.brooks@mailbox.example | Raleigh, NC | Cast Iron Skillet ×1; Electric Kettle 1.7L ×1 | $100.00 | $0.00 | $100.00 | Visa | Standard | delivered | — | — |
| JL-10439 | 2026-08-16 18:55 | wyatt.okafor@mailbox.example | Atlanta, GA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | RT-20078, RF-30113 | — |
| JL-10440 | 2026-08-16 19:50 | marcus.singh@webmail.example | Honolulu, HI | Scented Soy Candle ×2 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | RT-20103, RF-30123 | — |
| JL-10441 | 2026-08-16 19:51 | henry.young@webmail.example | Orlando, FL | Ceramic Planter Set ×2; LED Desk Lamp ×2 | $133.00 | $0.00 | $133.00 | American Express | Standard | delivered | — | — |
| JL-10442 | 2026-08-16 21:32 | nora.okafor@webmail.example | Seattle, WA | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | Visa | Express | delivered | RT-20073, RF-30106 | — |
| JL-10443 | 2026-08-17 10:20 | amelia.walker@mailbox.example | Philadelphia, PA | Wool Throw Blanket ×1; Oak Side Table ×1; Scented Soy Candle ×1 | $209.00 | $0.00 | $209.00 | PayPal | Standard | delivered | RT-20104 | — |
| JL-10444 | 2026-08-17 10:32 | scarlett.ramirez44@inbox.example | Atlanta, GA | Wool Throw Blanket ×1 | $68.00 | $12.99 | $80.99 | PayPal | Express | delivered | — | — |
| JL-10445 | 2026-08-17 12:37 | diego.sanders64@mailbox.example | Orlando, FL | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | PayPal | Standard | delivered | — | — |
| JL-10446 | 2026-08-17 13:27 | owen.morgan@inbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×1 | $63.99 | $0.00 | $63.99 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10447 | 2026-08-17 17:33 | noah.carter89@mailbox.example | Milwaukee, WI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10448 | 2026-08-17 18:42 | isaac.reyes50@inbox.example | Austin, TX | Cast Iron Skillet ×1; Ceramic Pour-Over Coffee Set ×1 | $97.00 | $0.00 | $97.00 | PayPal | Standard | delivered | RT-20082, RF-30104 | — |
| JL-10449 | 2026-08-18 07:16 | keisha.ellis@mailbox.example | Burlington, VT | LED Desk Lamp ×1; Linen Napkins (Set of 4) ×1 | $53.00 | $0.00 | $53.00 | Mastercard | Standard | delivered | — | — |
| JL-10450 | 2026-08-18 07:44 | mei.zimmerman@webmail.example | Chicago, IL | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | RF-30084, INV-50015 | — |
| JL-10451 | 2026-08-18 10:38 | zoey.zimmerman@webmail.example | Indianapolis, IN | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | Delivered after estimated window |
| JL-10452 | 2026-08-18 10:52 | evelyn.daniels53@inbox.example | New Orleans, LA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10453 | 2026-08-18 13:17 | levi.jensen@webmail.example | Tampa, FL | Juniper Lane Gift Card ×2 ($100.00 card) | $200.00 | $0.00 | $200.00 | Visa | Email (digital) | delivered | — | — |
| JL-10454 | 2026-08-18 14:37 | ethan.martinez40@webmail.example | Des Moines, IA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10455 | 2026-08-18 16:08 | arjun.owens58@webmail.example | Raleigh, NC | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | — | — |
| JL-10456 | 2026-08-18 16:56 | aria.kim21@mailbox.example | Orlando, FL | Adjustable Phone Stand ×1 | $15.00 | $12.99 | $27.99 | Juniper Lane gift card | Express | delivered | WC-40026 | — |
| JL-10457 | 2026-08-18 17:23 | ingrid.kim57@inbox.example | Anchorage, AK | Wireless Earbuds Pro ×1; Ceramic Planter Set ×2; Ceramic Pour-Over Coffee Set ×1 | $185.00 | $0.00 | $185.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10458 | 2026-08-18 18:42 | wyatt.okafor@mailbox.example | Atlanta, GA | Linen Napkins (Set of 4) ×2; Ceramic Pour-Over Coffee Set ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10459 | 2026-08-18 19:59 | priya.reyes@webmail.example | Anchorage, AK | Wireless Earbuds Pro ×1; Cast Iron Skillet ×1 | $134.00 | $0.00 | $134.00 | Mastercard | Standard | delivered | — | — |
| JL-10460 | 2026-08-19 06:35 | grace.gray9@inbox.example | Baltimore, MD | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10461 | 2026-08-19 07:54 | henry.hughes66@webmail.example | Orlando, FL | Adjustable Phone Stand ×11 | $165.00 | $0.00 | $165.00 | PayPal | Standard | cancelled | RF-30069 | Cancelled 2026-08-19 13:00: More than 10 units of one product; stock limited — support contacted customer first |
| JL-10462 | 2026-08-19 08:52 | abigail.bishop@mailbox.example | New Orleans, LA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | PayPal | Standard | delivered | — | — |
| JL-10463 | 2026-08-19 09:17 | evelyn.okafor78@mailbox.example | Houston, TX | Wireless Earbuds Pro ×1; Ceramic Pour-Over Coffee Set ×1 | $121.00 | $12.99 | $133.99 | Juniper Lane gift card | Express | delivered | RT-20096, RF-30120 | — |
| JL-10464 | 2026-08-19 12:56 | isaac.owens@webmail.example | Las Vegas, NV | Ceramic Planter Set ×1; Smart Plug (2-Pack) ×1 | $57.00 | $12.99 | $69.99 | Mastercard | Express | delivered | — | — |
| JL-10465 | 2026-08-19 16:30 | nathan.yamamoto@mailbox.example | Milwaukee, WI | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $74.49 | $0.00 | $74.49 | PayPal | Standard | delivered | WC-40034 | — |
| JL-10466 | 2026-08-20 06:17 | tessa.brooks@webmail.example | Milwaukee, WI | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Visa | Standard | delivered | RT-20149 | — |
| JL-10467 | 2026-08-20 11:49 | dylan.foster@mailbox.example | Baltimore, MD | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10468 | 2026-08-20 12:49 | ella.zimmerman@webmail.example | Detroit, MI | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | — | — |
| JL-10469 | 2026-08-20 14:41 | ella.perry@webmail.example | Houston, TX | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Mastercard | Standard | delivered | — | — |
| JL-10470 | 2026-08-20 17:41 | elijah.carter@mailbox.example | Richmond, VA | Electric Kettle 1.7L ×1; Scented Soy Candle ×1; Wireless Earbuds Pro ×1; Wool Throw Blanket ×1 | $204.00 | $0.00 | $204.00 | Visa | Standard | delivered | RT-20110, RF-30142 | — |
| JL-10471 | 2026-08-20 19:50 | henry.yamamoto72@inbox.example | Nashville, TN | Wool Throw Blanket ×3 | $204.00 | $0.00 | $204.00 | Visa | Standard | delivered | — | — |
| JL-10472 | 2026-08-20 21:38 | gabriel.jensen@mailbox.example | Philadelphia, PA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10473 | 2026-08-21 06:02 | nathan.kelly@webmail.example | Dallas, TX | Wireless Earbuds Pro ×1; Personalised Leather Notebook ×1 (emboss "A. Rivera") | $108.00 | $0.00 | $108.00 | Visa | Standard | delivered | RT-20083, RF-30105 | — |
| JL-10474 | 2026-08-21 07:20 | aaliyah.gray72@webmail.example | Des Moines, IA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | — | — |
| JL-10475 | 2026-08-21 08:59 | chloe.anderson30@mailbox.example | Buffalo, NY | Smart Plug (2-Pack) ×1 | $25.00 | $12.99 | $37.99 | Visa | Express | delivered | — | — |
| JL-10476 | 2026-08-21 09:57 | harper.morgan82@webmail.example | Des Moines, IA | LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $74.49 | $0.00 | $74.49 | Mastercard | Standard | delivered | — | — |
| JL-10477 | 2026-08-21 12:37 | nathan.perry@inbox.example | Richmond, VA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | American Express | Standard | delivered | — | — |
| JL-10478 | 2026-08-21 16:14 | mason.iyer@webmail.example | Phoenix, AZ | LED Desk Lamp ×2; Scented Soy Candle ×1; Wireless Earbuds Pro ×2 | $239.00 | $12.99 | $251.99 | Visa | Express | delivered | RT-20088, RF-30116 | — |
| JL-10479 | 2026-08-21 16:56 | soren.mitchell@mailbox.example | Austin, TX | Wireless Earbuds Pro ×2 | $158.00 | $0.00 | $158.00 | PayPal | Standard | delivered | RF-30189, WC-40045 | — |
| JL-10480 | 2026-08-21 17:51 | caleb.jensen37@inbox.example | Los Angeles, CA | Electric Kettle 1.7L ×2 | $90.00 | $0.00 | $90.00 | Mastercard | Standard | delivered | WC-40061 | — |
| JL-10481 | 2026-08-21 18:20 | mason.turner9@inbox.example | Richmond, VA | Bluetooth Speaker Mini ×2 | $79.98 | $0.00 | $79.98 | PayPal | Standard | cancelled | RF-30076 | Cancelled 2026-08-22 09:31: Customer request — ordered wrong item |
| JL-10482 | 2026-08-21 19:00 | wyatt.ingram@mailbox.example | Washington, DC | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10483 | 2026-08-21 21:48 | owen.bennett24@webmail.example | Dallas, TX | Scented Soy Candle ×3; Bluetooth Speaker Mini ×1; Adjustable Phone Stand ×1 | $90.99 | $0.00 | $90.99 | Juniper Lane gift card | Standard | delivered | RT-20086 | — |
| JL-10484 | 2026-08-21 22:47 | olivia.hughes41@inbox.example | Louisville, KY | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | cancelled | RF-30075 | Cancelled 2026-08-21 23:12: Customer request — found item elsewhere |
| JL-10485 | 2026-08-22 10:48 | wyatt.nelson66@mailbox.example | Nashville, TN | Linen Napkins (Set of 4) ×1; Smart Plug (2-Pack) ×1 | $43.50 | $4.99 | $48.49 | Visa | Standard | delivered | — | — |
| JL-10486 | 2026-08-22 15:02 | caleb.iyer@inbox.example | Charlotte, NC | Wireless Earbuds Pro ×1; Cast Iron Skillet ×1 | $134.00 | $0.00 | $134.00 | Visa | Standard | delivered | RT-20084 | — |
| JL-10487 | 2026-08-22 21:26 | maya.lopez39@inbox.example | Honolulu, HI | Bamboo Cutting Board ×1; Adjustable Phone Stand ×1 | $39.00 | $4.99 | $43.99 | Visa | Standard | delivered | RT-20087 | — |
| JL-10488 | 2026-08-23 07:51 | arjun.petrov@inbox.example | Portland, ME | Electric Kettle 1.7L ×1; Bluetooth Speaker Mini ×1 | $84.99 | $0.00 | $84.99 | Mastercard | Standard | delivered | — | — |
| JL-10489 | 2026-08-23 11:42 | tamara.xu@mailbox.example | Charlotte, NC | Smart Plug (2-Pack) ×1; Ceramic Pour-Over Coffee Set ×1 | $67.00 | $0.00 | $67.00 | PayPal | Standard | delivered | WC-40031 | — |
| JL-10490 | 2026-08-23 21:55 | amelia.brooks34@webmail.example | Kansas City, MO | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Mastercard | Express | delivered | — | — |
| JL-10491 | 2026-08-24 09:03 | mia.fischer@inbox.example | Nashville, TN | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | Mastercard | Express | delivered | — | Delivered after estimated window |
| JL-10492 | 2026-08-24 09:42 | soren.jackson@webmail.example | Los Angeles, CA | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Mastercard | Standard | cancelled | RF-30077 | Cancelled 2026-08-24 12:09: Customer request — found item elsewhere |
| JL-10493 | 2026-08-24 11:28 | mason.iyer@inbox.example | Nashville, TN | Electric Kettle 1.7L ×1; Bamboo Cutting Board ×1 | $69.00 | $0.00 | $69.00 | Mastercard | Standard | delivered | — | — |
| JL-10494 | 2026-08-24 12:20 | owen.carter56@mailbox.example | Charlotte, NC | Wool Throw Blanket ×3 | $204.00 | $12.99 | $216.99 | PayPal | Express | delivered | — | — |
| JL-10495 | 2026-08-24 16:40 | liam.bennett@webmail.example | Oklahoma City, OK | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10496 | 2026-08-24 17:09 | liam.rossi@mailbox.example | Detroit, MI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10497 | 2026-08-24 19:55 | ella.harris17@webmail.example | Kansas City, MO | LED Desk Lamp ×1; Wool Throw Blanket ×1; Electric Kettle 1.7L ×1 | $147.50 | $0.00 | $147.50 | American Express | Standard | delivered | RT-20091, RF-30114 | — |
| JL-10498 | 2026-08-25 08:45 | lucia.ingram@webmail.example | New Orleans, LA | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10499 | 2026-08-25 09:03 | nathan.fischer80@webmail.example | Minneapolis, MN | Bluetooth Speaker Mini ×1; Cast Iron Skillet ×1 | $94.99 | $0.00 | $94.99 | Visa | Standard | delivered | WC-40035 | — |
| JL-10500 | 2026-08-25 10:19 | jackson.patel@mailbox.example | Cleveland, OH | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | American Express | Email (digital) | delivered | — | — |
| JL-10501 | 2026-08-25 13:06 | marcus.foster18@webmail.example | Des Moines, IA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | RT-20111, RF-30134 | — |
| JL-10502 | 2026-08-25 14:24 | olivia.carter39@mailbox.example | Baltimore, MD | Electric Kettle 1.7L ×1; Smart Plug (2-Pack) ×2; LED Desk Lamp ×1 | $129.50 | $0.00 | $129.50 | PayPal | Standard | delivered | — | — |
| JL-10503 | 2026-08-25 19:01 | julian.singh@webmail.example | Washington, DC | Bamboo Cutting Board ×1; LED Desk Lamp ×1; Linen Napkins (Set of 4) ×1 | $77.00 | $0.00 | $77.00 | Visa | Standard | delivered | — | — |
| JL-10504 | 2026-08-26 06:25 | chloe.ellis@inbox.example | Cleveland, OH | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | American Express | Email (digital) | delivered | — | — |
| JL-10505 | 2026-08-26 08:54 | harper.vasquez20@mailbox.example | Louisville, KY | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Mastercard | Express | delivered | — | — |
| JL-10506 | 2026-08-26 11:40 | lily.petrov@webmail.example | San Diego, CA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10507 | 2026-08-26 13:01 | rachel.vasquez99@inbox.example | San Diego, CA | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | Visa | Express | delivered | RF-30099, DMG-55006 | — |
| JL-10508 | 2026-08-26 13:15 | lucas.kelly51@inbox.example | Des Moines, IA | Personalised Leather Notebook ×1 (emboss "Class of 2026"); Bamboo Cutting Board ×3 | $101.00 | $0.00 | $101.00 | PayPal | Standard | delivered | — | — |
| JL-10509 | 2026-08-26 13:53 | lucas.lewis90@inbox.example | Las Vegas, NV | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10510 | 2026-08-26 16:30 | grace.sanders47@webmail.example | Des Moines, IA | Electric Kettle 1.7L ×1; Ceramic Planter Set ×1 | $77.00 | $0.00 | $77.00 | Mastercard | Standard | delivered | — | — |
| JL-10511 | 2026-08-26 17:17 | henry.daniels40@inbox.example | Los Angeles, CA | Personalised Leather Notebook ×1 (emboss "Thank you, Ms. P") | $29.00 | $12.99 | $41.99 | Mastercard | Express | delivered | — | — |
| JL-10512 | 2026-08-26 17:51 | harper.vasquez20@mailbox.example | Louisville, KY | Bluetooth Speaker Mini ×1; Ceramic Pour-Over Coffee Set ×1 | $81.99 | $0.00 | $81.99 | PayPal | Standard | delivered | — | — |
| JL-10513 | 2026-08-26 18:13 | arjun.okafor@mailbox.example | Los Angeles, CA | Electric Kettle 1.7L ×3 | $135.00 | $0.00 | $135.00 | Mastercard | Standard | delivered | — | — |
| JL-10514 | 2026-08-27 08:02 | harper.walker@webmail.example | Phoenix, AZ | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | American Express | Standard | delivered | — | — |
| JL-10515 | 2026-08-27 08:53 | emma.flores@mailbox.example | Milwaukee, WI | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10516 | 2026-08-27 08:59 | mia.nelson29@webmail.example | San Francisco, CA | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Mastercard | Standard | delivered | — | — |
| JL-10517 | 2026-08-27 09:42 | mateo.petrov@mailbox.example | Cleveland, OH | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10518 | 2026-08-27 13:43 | evelyn.gray92@mailbox.example | Charlotte, NC | Adjustable Phone Stand ×1; Bluetooth Speaker Mini ×1 | $54.99 | $0.00 | $54.99 | PayPal | Standard | delivered | — | — |
| JL-10519 | 2026-08-27 19:56 | nathan.young@inbox.example | Anchorage, AK | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | PayPal | Express | delivered | — | — |
| JL-10520 | 2026-08-28 03:08 | mia.bennett34@webmail.example | Austin, TX | Bluetooth Speaker Mini ×1; Wireless Earbuds Pro ×1 | $118.99 | $0.00 | $118.99 | Mastercard | Standard | delivered | RT-20119, RF-30154 | — |
| JL-10521 | 2026-08-28 10:09 | isabella.johnson@mailbox.example | Las Vegas, NV | Ceramic Planter Set ×1; Linen Napkins (Set of 4) ×2 | $69.00 | $12.99 | $81.99 | Visa | Express | delivered | RT-20153 | — |
| JL-10522 | 2026-08-28 11:07 | evelyn.ellis@webmail.example | Philadelphia, PA | Oak Side Table ×1; Bluetooth Speaker Mini ×1 | $168.99 | $0.00 | $168.99 | Mastercard | Standard | delivered | RT-20098, RF-30121 | — |
| JL-10523 | 2026-08-28 13:33 | sophia.gupta45@webmail.example | Albuquerque, NM | Personalised Leather Notebook ×2 (emboss "Thank you, Ms. P"); Cast Iron Skillet ×1 | $113.00 | $0.00 | $113.00 | Mastercard | Standard | delivered | — | — |
| JL-10524 | 2026-08-28 15:35 | levi.singh53@mailbox.example | Raleigh, NC | Ceramic Planter Set ×2 | $64.00 | $0.00 | $64.00 | Visa | Standard | cancelled | RF-30088 | Cancelled 2026-08-29 03:19: Customer request — duplicate order |
| JL-10525 | 2026-08-28 15:50 | brandon.reyes75@inbox.example | Minneapolis, MN | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | American Express | Standard | delivered | — | — |
| JL-10526 | 2026-08-28 15:58 | hiro.chen72@webmail.example | Los Angeles, CA | Cast Iron Skillet ×1 | $55.00 | $12.99 | $67.99 | American Express | Express | delivered | — | — |
| JL-10527 | 2026-08-29 01:41 | abigail.kowalski72@webmail.example | Minneapolis, MN | Personalised Leather Notebook ×2 (emboss "Ben's Notes"); Bamboo Cutting Board ×1; Smart Plug (2-Pack) ×1 | $107.00 | $0.00 | $107.00 | American Express | Standard | delivered | — | — |
| JL-10528 | 2026-08-29 02:22 | owen.xu60@inbox.example | Portland, ME | Wireless Earbuds Pro ×1; Bamboo Cutting Board ×1 | $103.00 | $0.00 | $103.00 | Visa | Standard | delivered | RT-20094, RF-30118 | — |
| JL-10529 | 2026-08-29 08:17 | wyatt.davis1@webmail.example | Raleigh, NC | Scented Soy Candle ×1; Smart Plug (2-Pack) ×1 | $37.00 | $4.99 | $41.99 | PayPal | Standard | delivered | — | — |
| JL-10530 | 2026-08-29 10:58 | aiden.carter97@mailbox.example | Buffalo, NY | Linen Napkins (Set of 4) ×1; Bluetooth Speaker Mini ×1 | $58.49 | $0.00 | $58.49 | Visa | Standard | delivered | — | — |
| JL-10531 | 2026-08-29 16:07 | scarlett.walker@inbox.example | Washington, DC | Bamboo Cutting Board ×3 | $72.00 | $0.00 | $72.00 | Visa | Standard | delivered | — | — |
| JL-10532 | 2026-08-29 20:52 | evelyn.yamamoto63@webmail.example | Burlington, VT | Adjustable Phone Stand ×2; Wireless Earbuds Pro ×3; Cast Iron Skillet ×1 | $322.00 | $0.00 | $322.00 | American Express | Standard | delivered | — | — |
| JL-10533 | 2026-08-30 07:38 | chloe.okafor@inbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Ceramic Planter Set ×2; Scented Soy Candle ×1 | $100.00 | $0.00 | $100.00 | PayPal | Standard | delivered | — | — |
| JL-10534 | 2026-08-30 10:51 | chloe.walsh21@mailbox.example | Detroit, MI | Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×1; Wireless Earbuds Pro ×1; LED Desk Lamp ×2 | $211.99 | $0.00 | $211.99 | Visa | Standard | delivered | — | — |
| JL-10535 | 2026-08-30 11:54 | emma.reyes97@mailbox.example | Detroit, MI | Bamboo Cutting Board ×3 | $72.00 | $0.00 | $72.00 | Visa | Standard | delivered | — | — |
| JL-10536 | 2026-08-31 09:56 | omar.morgan99@mailbox.example | Phoenix, AZ | Bluetooth Speaker Mini ×1; Bamboo Cutting Board ×1 | $63.99 | $0.00 | $63.99 | Mastercard | Standard | delivered | — | — |
| JL-10537 | 2026-08-31 11:57 | harper.walsh@webmail.example | Columbus, OH | Bluetooth Speaker Mini ×3; Scented Soy Candle ×1 | $131.97 | $0.00 | $131.97 | Visa | Standard | delivered | RT-20112, RF-30137 | — |
| JL-10538 | 2026-08-31 17:02 | jamal.zimmerman@inbox.example | Philadelphia, PA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | RT-20093 | — |
| JL-10539 | 2026-08-31 17:58 | aiden.kim91@inbox.example | Milwaukee, WI | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Mastercard | Standard | delivered | — | — |
| JL-10540 | 2026-08-31 18:46 | ava.ingram41@inbox.example | Charlotte, NC | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Mastercard | Express | delivered | — | — |
| JL-10541 | 2026-08-31 21:51 | aaliyah.alvarez@mailbox.example | Orlando, FL | Bamboo Cutting Board ×1; Wool Throw Blanket ×1; Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "J\&M 2026") | $133.00 | $12.99 | $145.99 | Mastercard | Express | delivered | — | — |
| JL-10542 | 2026-09-01 11:18 | ingrid.anderson@webmail.example | Anchorage, AK | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10543 | 2026-09-01 16:54 | maya.davis74@inbox.example | Atlanta, GA | Wireless Earbuds Pro ×1; Ceramic Planter Set ×1; Linen Napkins (Set of 4) ×1; Bluetooth Speaker Mini ×2 | $209.48 | $0.00 | $209.48 | Mastercard | Standard | delivered | — | Delivered after estimated window |
| JL-10544 | 2026-09-01 17:05 | lucia.sanders92@webmail.example | Kansas City, MO | Scented Soy Candle ×1; Bamboo Cutting Board ×1; Linen Napkins (Set of 4) ×1 | $54.50 | $0.00 | $54.50 | Mastercard | Standard | delivered | — | — |
| JL-10545 | 2026-09-01 18:04 | henry.edwards95@webmail.example | Tampa, FL | Personalised Leather Notebook ×1 (emboss "For Maya") | $29.00 | $4.99 | $33.99 | Mastercard | Standard | delivered | — | — |
| JL-10546 | 2026-09-01 19:17 | ingrid.owens@inbox.example | Albuquerque, NM | Electric Kettle 1.7L ×2; Wireless Earbuds Pro ×3; LED Desk Lamp ×1 | $361.50 | $12.99 | $374.49 | Mastercard | Express | delivered | RT-20099, RF-30128 | — |
| JL-10547 | 2026-09-02 01:10 | tamara.nguyen@mailbox.example | Los Angeles, CA | Cast Iron Skillet ×1; Electric Kettle 1.7L ×1; LED Desk Lamp ×1 | $134.50 | $12.99 | $147.49 | Visa | Express | delivered | — | — |
| JL-10548 | 2026-09-02 10:18 | nora.reyes@mailbox.example | Louisville, KY | Bluetooth Speaker Mini ×1; Ceramic Pour-Over Coffee Set ×1; Scented Soy Candle ×1 | $93.99 | $0.00 | $93.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10549 | 2026-09-02 13:24 | diego.kowalski42@webmail.example | Pittsburgh, PA | Wool Throw Blanket ×1; Ceramic Planter Set ×1 | $100.00 | $0.00 | $100.00 | Visa | Standard | delivered | — | — |
| JL-10550 | 2026-09-02 14:13 | jamal.donovan5@mailbox.example | Cleveland, OH | Oak Side Table ×1; Cast Iron Skillet ×1; Scented Soy Candle ×1 | $196.00 | $0.00 | $196.00 | American Express | Standard | delivered | — | — |
| JL-10551 | 2026-09-02 15:42 | jackson.kim@webmail.example | Charlotte, NC | Ceramic Planter Set ×2; Bluetooth Speaker Mini ×1; Linen Napkins (Set of 4) ×2 | $140.99 | $12.99 | $153.98 | Mastercard | Express | delivered | WC-40046 | — |
| JL-10552 | 2026-09-02 23:24 | ingrid.nelson@mailbox.example | New York, NY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | American Express | Standard | delivered | RT-20101, RF-30124 | — |
| JL-10553 | 2026-09-03 02:35 | caleb.kowalski@mailbox.example | Denver, CO | Linen Napkins (Set of 4) ×1; Smart Plug (2-Pack) ×1 | $43.50 | $12.99 | $56.49 | Mastercard | Express | delivered | RT-20106, RF-30125 | — |
| JL-10554 | 2026-09-03 11:16 | abigail.davis66@inbox.example | Des Moines, IA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | American Express | Standard | delivered | — | Delivered after estimated window |
| JL-10555 | 2026-09-03 11:36 | brandon.patel14@webmail.example | Anchorage, AK | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | WC-40050 | — |
| JL-10556 | 2026-09-03 11:44 | aiden.lopez@inbox.example | Tampa, FL | Linen Napkins (Set of 4) ×1; Ceramic Pour-Over Coffee Set ×2; Scented Soy Candle ×1 | $114.50 | $0.00 | $114.50 | Juniper Lane gift card | Standard | delivered | RT-20125, RF-30164 | — |
| JL-10557 | 2026-09-03 18:49 | owen.young64@inbox.example | Columbus, OH | Cast Iron Skillet ×1; Adjustable Phone Stand ×1; Ceramic Planter Set ×1 | $102.00 | $12.99 | $114.99 | PayPal | Express | delivered | — | — |
| JL-10558 | 2026-09-03 19:33 | gabriel.vasquez@webmail.example | Detroit, MI | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10559 | 2026-09-04 07:31 | hazel.hughes26@mailbox.example | Miami, FL | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | — | — |
| JL-10560 | 2026-09-04 13:33 | mateo.petrov36@inbox.example | Richmond, VA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10561 | 2026-09-04 13:35 | aria.hughes@mailbox.example | Detroit, MI | Bluetooth Speaker Mini ×1; Cast Iron Skillet ×1 | $94.99 | $12.99 | $107.98 | Mastercard | Express | delivered | — | — |
| JL-10562 | 2026-09-04 16:17 | omar.kelly90@mailbox.example | Minneapolis, MN | Scented Soy Candle ×1; LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $86.49 | $12.99 | $99.48 | American Express | Express | delivered | RT-20113, RF-30148 | — |
| JL-10563 | 2026-09-04 16:58 | mateo.vasquez@inbox.example | Atlanta, GA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | American Express | Email (digital) | delivered | — | — |
| JL-10564 | 2026-09-04 20:23 | ethan.hammond26@mailbox.example | Miami, FL | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10565 | 2026-09-05 11:26 | lucas.nguyen@webmail.example | Buffalo, NY | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Juniper Lane gift card | Standard | delivered | RT-20136, RF-30167 | — |
| JL-10566 | 2026-09-05 14:01 | mason.quinn6@mailbox.example | Portland, ME | Adjustable Phone Stand ×2 | $30.00 | $4.99 | $34.99 | Visa | Standard | delivered | — | — |
| JL-10567 | 2026-09-05 16:48 | abigail.harris63@inbox.example | Portland, ME | Electric Kettle 1.7L ×1; Wireless Earbuds Pro ×1 | $124.00 | $0.00 | $124.00 | Mastercard | Standard | delivered | RT-20164 | — |
| JL-10568 | 2026-09-05 20:43 | diego.garcia@inbox.example | Houston, TX | Ceramic Planter Set ×1; Wireless Earbuds Pro ×1 | $111.00 | $0.00 | $111.00 | PayPal | Standard | delivered | WC-40037 | — |
| JL-10569 | 2026-09-06 00:25 | nathan.perry@inbox.example | Richmond, VA | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Visa | Express | delivered | RT-20116, RF-30145 | — |
| JL-10570 | 2026-09-06 09:13 | harper.morgan82@webmail.example | Des Moines, IA | Linen Napkins (Set of 4) ×2 | $37.00 | $4.99 | $41.99 | Visa | Standard | delivered | — | — |
| JL-10571 | 2026-09-06 09:40 | diego.sanders64@mailbox.example | Orlando, FL | Ceramic Pour-Over Coffee Set ×1; Smart Plug (2-Pack) ×1; Cast Iron Skillet ×1 | $122.00 | $0.00 | $122.00 | Visa | Standard | cancelled | RF-30101 | Cancelled 2026-09-06 17:47: Customer request — changed mind |
| JL-10572 | 2026-09-06 10:41 | levi.sanders95@mailbox.example | Austin, TX | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Mastercard | Standard | delivered | — | — |
| JL-10573 | 2026-09-06 17:56 | abigail.daniels36@inbox.example | Honolulu, HI | Ceramic Pour-Over Coffee Set ×1; Linen Napkins (Set of 4) ×1 | $60.50 | $0.00 | $60.50 | Mastercard | Standard | delivered | — | — |
| JL-10574 | 2026-09-07 14:14 | brandon.edwards@mailbox.example | Philadelphia, PA | LED Desk Lamp ×1 | $34.50 | $12.99 | $47.49 | PayPal | Express | delivered | — | — |
| JL-10575 | 2026-09-07 17:59 | mateo.ramirez90@mailbox.example | Louisville, KY | Ceramic Pour-Over Coffee Set ×2 | $84.00 | $0.00 | $84.00 | PayPal | Standard | delivered | RT-20100, RF-30131 | — |
| JL-10576 | 2026-09-07 20:13 | lucia.patel@mailbox.example | San Diego, CA | Wool Throw Blanket ×1; Bamboo Cutting Board ×1 | $92.00 | $0.00 | $92.00 | Mastercard | Standard | delivered | RT-20157 | — |
| JL-10577 | 2026-09-08 12:46 | mei.owens56@mailbox.example | San Diego, CA | Wool Throw Blanket ×2 | $136.00 | $12.99 | $148.99 | Mastercard | Express | delivered | — | — |
| JL-10578 | 2026-09-08 13:54 | diego.singh@inbox.example | Boston, MA | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10579 | 2026-09-08 14:39 | tessa.mitchell81@inbox.example | Honolulu, HI | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | cancelled | RF-30102 | Cancelled 2026-09-08 21:36: Customer request — changed mind |
| JL-10580 | 2026-09-08 17:26 | mei.gupta58@webmail.example | Austin, TX | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10581 | 2026-09-08 18:24 | james.owens@inbox.example | Washington, DC | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | American Express | Standard | lost | INV-50016 | — |
| JL-10582 | 2026-09-08 18:39 | wyatt.patel@webmail.example | Los Angeles, CA | Adjustable Phone Stand ×1; LED Desk Lamp ×1; Smart Plug (2-Pack) ×1 | $74.50 | $0.00 | $74.50 | Mastercard | Standard | delivered | — | — |
| JL-10583 | 2026-09-08 19:37 | noah.foster48@inbox.example | Seattle, WA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Mastercard | Standard | delivered | RT-20115, RF-30140 | — |
| JL-10584 | 2026-09-09 07:55 | liam.nelson11@webmail.example | Las Vegas, NV | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Mastercard | Standard | delivered | — | — |
| JL-10585 | 2026-09-09 09:25 | caleb.lewis7@inbox.example | Dallas, TX | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | RT-20124, RF-30146 | — |
| JL-10586 | 2026-09-09 16:29 | grace.walker28@inbox.example | Las Vegas, NV | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10587 | 2026-09-09 17:07 | amelia.morgan64@inbox.example | Portland, OR | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10588 | 2026-09-10 08:35 | evelyn.gray@mailbox.example | Denver, CO | Adjustable Phone Stand ×1; Bluetooth Speaker Mini ×1 | $54.99 | $0.00 | $54.99 | Visa | Standard | delivered | RT-20175 | — |
| JL-10589 | 2026-09-10 13:15 | mia.nelson@mailbox.example | Baltimore, MD | Ceramic Planter Set ×1; Wireless Earbuds Pro ×1 | $111.00 | $12.99 | $123.99 | Visa | Express | delivered | WC-40041 | — |
| JL-10590 | 2026-09-10 16:58 | lucia.nguyen@mailbox.example | Charlotte, NC | Linen Napkins (Set of 4) ×1; Oak Side Table ×1; Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam"); Bamboo Cutting Board ×1 | $229.50 | $0.00 | $229.50 | Mastercard | Standard | delivered | RT-20118 | — |
| JL-10591 | 2026-09-11 07:04 | keisha.rossi@webmail.example | Oklahoma City, OK | Bluetooth Speaker Mini ×1; Electric Kettle 1.7L ×1; Wool Throw Blanket ×1 | $152.99 | $0.00 | $152.99 | Mastercard | Standard | delivered | — | Delivered after estimated window |
| JL-10592 | 2026-09-11 07:52 | mason.daniels86@webmail.example | Portland, OR | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | RT-20126, RF-30168 | Delivered after estimated window |
| JL-10593 | 2026-09-11 09:51 | hazel.ellis52@inbox.example | Baltimore, MD | Bluetooth Speaker Mini ×2 | $79.98 | $0.00 | $79.98 | Mastercard | Standard | delivered | — | — |
| JL-10594 | 2026-09-11 11:10 | liam.kim@webmail.example | Philadelphia, PA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | — | — |
| JL-10595 | 2026-09-11 11:42 | lucia.mitchell6@webmail.example | Baltimore, MD | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | RT-20154 | — |
| JL-10596 | 2026-09-11 13:34 | logan.thompson@inbox.example | Richmond, VA | Wool Throw Blanket ×3; Ceramic Planter Set ×1 | $236.00 | $12.99 | $248.99 | American Express | Express | delivered | RT-20114, RF-30132 | — |
| JL-10597 | 2026-09-11 15:06 | isaac.kim46@webmail.example | Minneapolis, MN | Smart Plug (2-Pack) ×1; Ceramic Pour-Over Coffee Set ×1 | $67.00 | $0.00 | $67.00 | American Express | Standard | delivered | — | — |
| JL-10598 | 2026-09-11 15:37 | aiden.rossi20@inbox.example | Denver, CO | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10599 | 2026-09-11 16:06 | mateo.perry@mailbox.example | Milwaukee, WI | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Visa | Express | delivered | — | — |
| JL-10600 | 2026-09-11 20:37 | levi.hughes37@mailbox.example | Providence, RI | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10601 | 2026-09-12 14:15 | logan.thompson@inbox.example | Richmond, VA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | — | — |
| JL-10602 | 2026-09-12 14:45 | fatima.fischer69@mailbox.example | Detroit, MI | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | RT-20107, RF-30138 | — |
| JL-10603 | 2026-09-12 16:00 | arjun.petrov@webmail.example | San Diego, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | RF-30122, INV-50018 | — |
| JL-10604 | 2026-09-12 18:19 | elijah.gupta@webmail.example | Denver, CO | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | PayPal | Standard | delivered | INV-50017 | — |
| JL-10605 | 2026-09-13 00:39 | liam.gray89@webmail.example | Seattle, WA | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | — | — |
| JL-10606 | 2026-09-13 06:07 | lily.donovan58@inbox.example | Atlanta, GA | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | American Express | Email (digital) | delivered | — | — |
| JL-10607 | 2026-09-13 10:38 | henry.vasquez@webmail.example | Honolulu, HI | Bamboo Cutting Board ×1; Ceramic Planter Set ×1 | $56.00 | $0.00 | $56.00 | PayPal | Standard | delivered | — | — |
| JL-10608 | 2026-09-13 14:06 | priya.walker29@mailbox.example | Portland, OR | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10609 | 2026-09-13 14:35 | tamara.edwards59@mailbox.example | Cleveland, OH | Bluetooth Speaker Mini ×1; Personalised Leather Notebook ×1 (emboss "Team Lead") | $68.99 | $0.00 | $68.99 | Visa | Standard | delivered | — | — |
| JL-10610 | 2026-09-13 17:24 | zoey.petrov@inbox.example | San Francisco, CA | LED Desk Lamp ×1; Cast Iron Skillet ×1 | $89.50 | $0.00 | $89.50 | Visa | Standard | delivered | WC-40055 | — |
| JL-10611 | 2026-09-13 20:43 | mia.iyer25@inbox.example | Minneapolis, MN | Smart Plug (2-Pack) ×2; Wireless Earbuds Pro ×1 | $129.00 | $0.00 | $129.00 | PayPal | Standard | delivered | — | — |
| JL-10612 | 2026-09-13 22:54 | dylan.campbell@webmail.example | Boston, MA | Adjustable Phone Stand ×3 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | — | — |
| JL-10613 | 2026-09-14 08:09 | arjun.davis@webmail.example | Milwaukee, WI | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10614 | 2026-09-14 09:19 | levi.davis@webmail.example | Seattle, WA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10615 | 2026-09-14 12:08 | arjun.martinez@inbox.example | Milwaukee, WI | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Visa | Standard | delivered | RT-20132, RF-30175 | — |
| JL-10616 | 2026-09-14 14:25 | rachel.harris@webmail.example | Minneapolis, MN | Electric Kettle 1.7L ×1; Adjustable Phone Stand ×1; Ceramic Planter Set ×1 | $92.00 | $0.00 | $92.00 | Mastercard | Standard | delivered | RT-20131, RF-30165 | — |
| JL-10617 | 2026-09-14 16:06 | wyatt.xu@inbox.example | Detroit, MI | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | PayPal | Standard | delivered | — | — |
| JL-10618 | 2026-09-14 19:02 | maya.novak@inbox.example | Philadelphia, PA | Cast Iron Skillet ×3; Bluetooth Speaker Mini ×2 | $244.98 | $12.99 | $257.97 | Juniper Lane gift card | Express | lost | INV-50019 | — |
| JL-10619 | 2026-09-14 21:40 | tessa.sanders83@inbox.example | Charlotte, NC | Linen Napkins (Set of 4) ×1; Smart Plug (2-Pack) ×1 | $43.50 | $4.99 | $48.49 | PayPal | Standard | delivered | — | — |
| JL-10620 | 2026-09-15 08:31 | scarlett.zimmerman@inbox.example | Louisville, KY | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | cancelled | RF-30112 | Cancelled 2026-09-15 12:51: Customer request — ordered wrong item |
| JL-10621 | 2026-09-15 09:11 | devon.alvarez@webmail.example | Miami, FL | Personalised Leather Notebook ×2 (emboss "Field Notes - LK"); Cast Iron Skillet ×1 | $113.00 | $12.99 | $125.99 | Visa | Express | delivered | — | — |
| JL-10622 | 2026-09-15 11:45 | james.xu@webmail.example | Pittsburgh, PA | Personalised Leather Notebook ×1 (emboss "Field Notes - LK"); Cast Iron Skillet ×1; Wireless Earbuds Pro ×1 | $163.00 | $0.00 | $163.00 | American Express | Standard | delivered | RT-20129, RF-30155 | — |
| JL-10623 | 2026-09-15 12:17 | maya.fischer@mailbox.example | Nashville, TN | Adjustable Phone Stand ×1; LED Desk Lamp ×1 | $49.50 | $4.99 | $54.49 | Mastercard | Standard | delivered | — | — |
| JL-10624 | 2026-09-15 14:37 | mason.iyer@inbox.example | Nashville, TN | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10625 | 2026-09-15 17:13 | nathan.garcia@mailbox.example | Pittsburgh, PA | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Visa | Express | delivered | WC-40048 | — |
| JL-10626 | 2026-09-15 18:34 | keisha.gray@webmail.example | Portland, ME | Electric Kettle 1.7L ×1; Bluetooth Speaker Mini ×1; Scented Soy Candle ×1 | $96.99 | $0.00 | $96.99 | PayPal | Standard | delivered | RT-20133 | — |
| JL-10627 | 2026-09-15 19:57 | ava.martinez@mailbox.example | Baltimore, MD | Bamboo Cutting Board ×1; Smart Plug (2-Pack) ×1 | $49.00 | $4.99 | $53.99 | Visa | Standard | delivered | — | — |
| JL-10628 | 2026-09-15 20:05 | arjun.xu@webmail.example | Orlando, FL | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10629 | 2026-09-16 10:11 | mateo.young@webmail.example | Raleigh, NC | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | — | — |
| JL-10630 | 2026-09-16 11:04 | chloe.foster42@mailbox.example | Seattle, WA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10631 | 2026-09-16 12:55 | amelia.turner64@inbox.example | Boston, MA | Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "J\&M 2026") | $41.00 | $4.99 | $45.99 | Visa | Standard | delivered | RT-20128 | — |
| JL-10632 | 2026-09-16 14:03 | gabriel.garcia1@mailbox.example | Denver, CO | Scented Soy Candle ×3; Ceramic Pour-Over Coffee Set ×1 | $78.00 | $0.00 | $78.00 | American Express | Standard | delivered | — | Delivered after estimated window |
| JL-10633 | 2026-09-16 15:05 | ella.sanders65@webmail.example | Milwaukee, WI | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10634 | 2026-09-16 17:35 | arjun.martinez@inbox.example | Milwaukee, WI | Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1 | $64.99 | $12.99 | $77.98 | Mastercard | Express | delivered | — | — |
| JL-10635 | 2026-09-17 00:48 | maya.kelly26@mailbox.example | Burlington, VT | Bamboo Cutting Board ×2 | $48.00 | $4.99 | $52.99 | Visa | Standard | delivered | — | — |
| JL-10636 | 2026-09-17 07:36 | ingrid.turner74@inbox.example | Indianapolis, IN | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | American Express | Standard | delivered | — | — |
| JL-10637 | 2026-09-17 08:08 | tamara.donovan@mailbox.example | Houston, TX | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | PayPal | Standard | delivered | — | — |
| JL-10638 | 2026-09-17 10:33 | evelyn.brooks@inbox.example | Indianapolis, IN | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | delivered | INV-50020 | — |
| JL-10639 | 2026-09-17 12:22 | brandon.harris20@mailbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×1 | $63.99 | $12.99 | $76.98 | PayPal | Express | delivered | WC-40075 | — |
| JL-10640 | 2026-09-17 13:20 | amelia.larson93@webmail.example | San Francisco, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | WC-40049 | — |
| JL-10641 | 2026-09-17 14:14 | arjun.iyer@mailbox.example | Orlando, FL | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10642 | 2026-09-17 18:37 | dylan.edwards1@mailbox.example | Louisville, KY | Personalised Leather Notebook ×1 (emboss "J\&M 2026"); Electric Kettle 1.7L ×1 | $74.00 | $0.00 | $74.00 | Visa | Standard | delivered | RT-20152, RF-30184 | — |
| JL-10643 | 2026-09-17 20:47 | olivia.anderson52@mailbox.example | Miami, FL | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | RT-20135, RF-30166 | — |
| JL-10644 | 2026-09-18 00:29 | james.alvarez34@mailbox.example | Seattle, WA | Ceramic Planter Set ×2; Scented Soy Candle ×1 | $76.00 | $0.00 | $76.00 | Mastercard | Standard | delivered | — | — |
| JL-10645 | 2026-09-18 11:55 | hiro.johnson@webmail.example | Washington, DC | Smart Plug (2-Pack) ×1; Adjustable Phone Stand ×1; Linen Napkins (Set of 4) ×1 | $58.50 | $12.99 | $71.49 | Visa | Express | delivered | — | — |
| JL-10646 | 2026-09-18 13:23 | gabriel.walsh31@inbox.example | New York, NY | Bamboo Cutting Board ×1; Personalised Leather Notebook ×1 (emboss "Class of 2026") | $53.00 | $0.00 | $53.00 | Mastercard | Standard | delivered | — | — |
| JL-10647 | 2026-09-19 03:00 | julian.petrov@mailbox.example | Austin, TX | Ceramic Planter Set ×2 | $64.00 | $12.99 | $76.99 | Mastercard | Express | delivered | RT-20146, RF-30176 | — |
| JL-10648 | 2026-09-19 08:33 | logan.sanders@webmail.example | Atlanta, GA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | PayPal | Standard | delivered | RT-20117, RF-30149 | — |
| JL-10649 | 2026-09-19 12:54 | chloe.quinn77@webmail.example | Portland, ME | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | lost | RF-30136, INV-50023 | — |
| JL-10650 | 2026-09-19 14:23 | elijah.foster@webmail.example | Seattle, WA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | PayPal | Standard | delivered | — | — |
| JL-10651 | 2026-09-19 20:06 | sophia.larson@webmail.example | Denver, CO | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10652 | 2026-09-19 20:26 | sophia.larson@webmail.example | Denver, CO | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10653 | 2026-09-19 21:38 | mateo.campbell75@mailbox.example | Omaha, NE | Bamboo Cutting Board ×1; LED Desk Lamp ×1; Wireless Earbuds Pro ×1 | $137.50 | $0.00 | $137.50 | Visa | Standard | delivered | — | — |
| JL-10654 | 2026-09-19 21:39 | jackson.nelson@webmail.example | Phoenix, AZ | Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1; Adjustable Phone Stand ×1; Ceramic Planter Set ×2 | $143.99 | $0.00 | $143.99 | Mastercard | Standard | delivered | RT-20150 | Delivered after estimated window |
| JL-10655 | 2026-09-20 08:19 | mateo.flores44@mailbox.example | Cleveland, OH | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Mastercard | Standard | delivered | — | — |
| JL-10656 | 2026-09-20 10:12 | maya.davis74@inbox.example | Atlanta, GA | Wireless Earbuds Pro ×3 | $237.00 | $0.00 | $237.00 | Visa | Standard | delivered | RT-20189 | — |
| JL-10657 | 2026-09-20 10:32 | liam.campbell@webmail.example | Charlotte, NC | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10658 | 2026-09-20 10:35 | elijah.walsh@inbox.example | Boise, ID | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | WC-40062 | — |
| JL-10659 | 2026-09-20 13:25 | priya.perry@webmail.example | Portland, ME | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Mastercard | Standard | delivered | — | — |
| JL-10660 | 2026-09-20 13:38 | devon.bishop77@webmail.example | Kansas City, MO | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | — | — |
| JL-10661 | 2026-09-20 14:16 | maya.rossi46@inbox.example | Des Moines, IA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10662 | 2026-09-20 17:13 | tessa.quinn@mailbox.example | Albuquerque, NM | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | — | — |
| JL-10663 | 2026-09-20 18:34 | mason.novak49@webmail.example | Louisville, KY | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | cancelled | RF-30117 | Cancelled 2026-09-20 22:57: Customer request — found item elsewhere |
| JL-10664 | 2026-09-20 18:47 | abigail.brooks@webmail.example | Portland, ME | Electric Kettle 1.7L ×1; Linen Napkins (Set of 4) ×1 | $63.50 | $0.00 | $63.50 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10665 | 2026-09-20 23:51 | ingrid.turner@inbox.example | Raleigh, NC | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Visa | Standard | delivered | INV-50022 | — |
| JL-10666 | 2026-09-21 08:12 | diego.edwards14@inbox.example | Oklahoma City, OK | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | DMG-55007 | — |
| JL-10667 | 2026-09-21 12:15 | scarlett.singh@webmail.example | Phoenix, AZ | Wireless Earbuds Pro ×1; Bamboo Cutting Board ×1 | $103.00 | $0.00 | $103.00 | Juniper Lane gift card | Standard | delivered | — | Delivered after estimated window |
| JL-10668 | 2026-09-21 15:43 | jamal.harris49@webmail.example | Orlando, FL | Adjustable Phone Stand ×2; Electric Kettle 1.7L ×2; LED Desk Lamp ×1 | $154.50 | $0.00 | $154.50 | PayPal | Standard | delivered | — | — |
| JL-10669 | 2026-09-21 15:53 | gabriel.owens63@inbox.example | Anchorage, AK | Oak Side Table ×1; Ceramic Planter Set ×1 | $161.00 | $0.00 | $161.00 | Mastercard | Standard | delivered | INV-50024 | — |
| JL-10670 | 2026-09-21 22:33 | keisha.jensen@inbox.example | Richmond, VA | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | American Express | Email (digital) | delivered | — | — |
| JL-10671 | 2026-09-22 09:58 | tamara.reyes@mailbox.example | Houston, TX | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | American Express | Standard | delivered | — | — |
| JL-10672 | 2026-09-22 10:08 | grace.sanders@webmail.example | Richmond, VA | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10673 | 2026-09-22 13:10 | caleb.nguyen@mailbox.example | Milwaukee, WI | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | — | — |
| JL-10674 | 2026-09-22 14:52 | priya.reyes44@webmail.example | Washington, DC | Adjustable Phone Stand ×1; Bluetooth Speaker Mini ×1; Scented Soy Candle ×1 | $66.99 | $0.00 | $66.99 | PayPal | Standard | delivered | — | — |
| JL-10675 | 2026-09-22 15:24 | caleb.gray@webmail.example | Des Moines, IA | Electric Kettle 1.7L ×1; Ceramic Planter Set ×1; Scented Soy Candle ×1 | $89.00 | $12.99 | $101.99 | Juniper Lane gift card | Express | delivered | WC-40058 | — |
| JL-10676 | 2026-09-22 16:12 | rachel.harris@webmail.example | Minneapolis, MN | Wireless Earbuds Pro ×1; Ceramic Pour-Over Coffee Set ×3 | $205.00 | $0.00 | $205.00 | Mastercard | Standard | delivered | RT-20137, RF-30183 | — |
| JL-10677 | 2026-09-22 16:41 | mateo.walker36@mailbox.example | Philadelphia, PA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | WC-40053 | — |
| JL-10678 | 2026-09-22 19:18 | james.morgan@webmail.example | New York, NY | Ceramic Pour-Over Coffee Set ×1; Electric Kettle 1.7L ×1 | $87.00 | $0.00 | $87.00 | Mastercard | Standard | delivered | RT-20176 | — |
| JL-10679 | 2026-09-23 02:33 | priya.quinn@inbox.example | Detroit, MI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | RT-20130, RF-30160 | — |
| JL-10680 | 2026-09-23 10:17 | emma.hughes42@webmail.example | Indianapolis, IN | Personalised Leather Notebook ×1 (emboss "Dad") | $29.00 | $12.99 | $41.99 | Visa | Express | delivered | — | — |
| JL-10681 | 2026-09-23 11:00 | sophia.donovan@inbox.example | Louisville, KY | Wireless Earbuds Pro ×1; Linen Napkins (Set of 4) ×2 | $116.00 | $0.00 | $116.00 | Visa | Standard | delivered | — | — |
| JL-10682 | 2026-09-23 13:46 | keisha.ingram64@inbox.example | New York, NY | LED Desk Lamp ×1; Linen Napkins (Set of 4) ×1 | $53.00 | $0.00 | $53.00 | American Express | Standard | delivered | RT-20158, RF-30201 | — |
| JL-10683 | 2026-09-23 16:44 | keisha.martinez9@mailbox.example | Las Vegas, NV | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | RT-20127, RF-30150 | — |
| JL-10684 | 2026-09-23 18:19 | abigail.larson@webmail.example | Pittsburgh, PA | Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1 | $64.99 | $0.00 | $64.99 | PayPal | Standard | delivered | RT-20140, RF-30188 | — |
| JL-10685 | 2026-09-23 19:28 | mia.ingram@mailbox.example | Washington, DC | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | — | — |
| JL-10686 | 2026-09-23 21:16 | james.flores35@webmail.example | Columbus, OH | Smart Plug (2-Pack) ×2 | $50.00 | $0.00 | $50.00 | Visa | Standard | delivered | — | — |
| JL-10687 | 2026-09-24 05:00 | evelyn.kowalski63@mailbox.example | Phoenix, AZ | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10688 | 2026-09-24 07:41 | abigail.flores@webmail.example | Columbus, OH | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10689 | 2026-09-24 10:05 | wyatt.reyes21@inbox.example | Anchorage, AK | Ceramic Planter Set ×1; Adjustable Phone Stand ×1 | $47.00 | $4.99 | $51.99 | Mastercard | Standard | delivered | — | — |
| JL-10690 | 2026-09-24 10:48 | lucas.kim@webmail.example | Dallas, TX | Wool Throw Blanket ×1; Ceramic Planter Set ×2 | $132.00 | $0.00 | $132.00 | Juniper Lane gift card | Standard | delivered | RT-20122, RF-30151 | — |
| JL-10691 | 2026-09-24 12:28 | evelyn.ingram37@mailbox.example | Portland, ME | Wireless Earbuds Pro ×2 | $158.00 | $12.99 | $170.99 | Visa | Express | delivered | INV-50021 | — |
| JL-10692 | 2026-09-24 13:46 | lucia.mitchell6@webmail.example | Baltimore, MD | Wool Throw Blanket ×1; Scented Soy Candle ×1 | $80.00 | $0.00 | $80.00 | Mastercard | Standard | delivered | — | — |
| JL-10693 | 2026-09-24 19:05 | aaliyah.singh@webmail.example | Portland, ME | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10694 | 2026-09-24 20:59 | lily.brooks68@inbox.example | Milwaukee, WI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10695 | 2026-09-24 22:44 | zoey.nelson53@webmail.example | Dallas, TX | Ceramic Planter Set ×1; Wireless Earbuds Pro ×1; Personalised Leather Notebook ×1 (emboss "Dad") | $140.00 | $0.00 | $140.00 | Visa | Standard | delivered | — | — |
| JL-10696 | 2026-09-25 00:19 | evelyn.okafor@inbox.example | Des Moines, IA | Wool Throw Blanket ×2; Electric Kettle 1.7L ×2; Scented Soy Candle ×1 | $238.00 | $0.00 | $238.00 | Visa | Standard | delivered | RT-20147, RF-30180 | — |
| JL-10697 | 2026-09-25 06:45 | henry.young@webmail.example | Orlando, FL | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | — | — |
| JL-10698 | 2026-09-25 12:31 | levi.singh4@inbox.example | Houston, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | — | — |
| JL-10699 | 2026-09-25 13:13 | omar.morgan99@mailbox.example | Phoenix, AZ | Ceramic Planter Set ×1; LED Desk Lamp ×1 | $66.50 | $0.00 | $66.50 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10700 | 2026-09-25 15:41 | mateo.yamamoto@mailbox.example | Honolulu, HI | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | INV-50025 | — |
| JL-10701 | 2026-09-26 11:28 | fatima.bennett@webmail.example | New York, NY | Oak Side Table ×1; Ceramic Planter Set ×1 | $161.00 | $0.00 | $161.00 | Visa | Standard | delivered | RT-20159, RF-30194 | — |
| JL-10702 | 2026-09-26 14:29 | tessa.carter@inbox.example | Milwaukee, WI | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | American Express | Standard | delivered | WC-40056 | — |
| JL-10703 | 2026-09-26 16:16 | lily.fischer@webmail.example | Chicago, IL | Linen Napkins (Set of 4) ×3; Wireless Earbuds Pro ×1; Bamboo Cutting Board ×1; Bluetooth Speaker Mini ×1 | $198.49 | $0.00 | $198.49 | Mastercard | Standard | delivered | — | — |
| JL-10704 | 2026-09-26 16:37 | olivia.quinn@webmail.example | Las Vegas, NV | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10705 | 2026-09-26 21:36 | diego.gray@webmail.example | Columbus, OH | Personalised Leather Notebook ×1 (emboss "Mom"); Smart Plug (2-Pack) ×1 | $54.00 | $12.99 | $66.99 | Visa | Express | delivered | INV-50026 | — |
| JL-10706 | 2026-09-27 11:49 | owen.sanders@mailbox.example | Portland, ME | Wool Throw Blanket ×1; Personalised Leather Notebook ×1 (emboss "Ben's Notes"); Electric Kettle 1.7L ×1 | $142.00 | $0.00 | $142.00 | Mastercard | Standard | delivered | — | — |
| JL-10707 | 2026-09-27 13:16 | scarlett.johnson83@mailbox.example | Portland, OR | Electric Kettle 1.7L ×1; Bluetooth Speaker Mini ×1; Bamboo Cutting Board ×1 | $108.99 | $0.00 | $108.99 | Visa | Standard | delivered | — | — |
| JL-10708 | 2026-09-27 15:14 | gabriel.johnson@mailbox.example | Denver, CO | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | RT-20141, RF-30182 | — |
| JL-10709 | 2026-09-27 18:20 | mia.turner52@inbox.example | Buffalo, NY | Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1 | $64.99 | $0.00 | $64.99 | Mastercard | Standard | cancelled | RF-30126 | Cancelled 2026-09-28 15:07: Customer request — duplicate order |
| JL-10710 | 2026-09-28 10:09 | maya.ramirez@mailbox.example | Baltimore, MD | Linen Napkins (Set of 4) ×1; Ceramic Planter Set ×1 | $50.50 | $0.00 | $50.50 | Juniper Lane gift card | Standard | cancelled | RF-30127 | Cancelled 2026-09-28 10:19: Customer request — ordered wrong item |
| JL-10711 | 2026-09-28 10:19 | mason.walsh99@webmail.example | Minneapolis, MN | Personalised Leather Notebook ×1 (emboss "A. Rivera"); Oak Side Table ×1; Bamboo Cutting Board ×1 | $182.00 | $0.00 | $182.00 | Visa | Standard | delivered | — | — |
| JL-10712 | 2026-09-28 14:44 | scarlett.hughes@inbox.example | Atlanta, GA | Cast Iron Skillet ×1; Wireless Earbuds Pro ×1; LED Desk Lamp ×1 | $168.50 | $0.00 | $168.50 | Visa | Standard | delivered | INV-50028 | — |
| JL-10713 | 2026-09-28 18:11 | harper.morgan30@webmail.example | Chicago, IL | Smart Plug (2-Pack) ×1; Adjustable Phone Stand ×2; Linen Napkins (Set of 4) ×1; Bamboo Cutting Board ×1 | $97.50 | $0.00 | $97.50 | American Express | Standard | delivered | — | — |
| JL-10714 | 2026-09-28 21:36 | devon.martinez@webmail.example | Salt Lake City, UT | Ceramic Planter Set ×1; Cast Iron Skillet ×1 | $87.00 | $0.00 | $87.00 | Visa | Standard | delivered | — | — |
| JL-10715 | 2026-09-29 10:49 | jackson.larson68@webmail.example | Nashville, TN | Bamboo Cutting Board ×2 | $48.00 | $12.99 | $60.99 | American Express | Express | delivered | — | — |
| JL-10716 | 2026-09-29 12:42 | isabella.ramirez84@inbox.example | Los Angeles, CA | Adjustable Phone Stand ×1; LED Desk Lamp ×1 | $49.50 | $4.99 | $54.49 | American Express | Standard | delivered | RT-20185 | — |
| JL-10717 | 2026-09-29 16:08 | logan.turner@webmail.example | Atlanta, GA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Mastercard | Standard | delivered | RT-20144 | — |
| JL-10718 | 2026-09-29 19:54 | abigail.martinez48@webmail.example | Detroit, MI | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Visa | Express | delivered | — | — |
| JL-10719 | 2026-09-29 22:25 | fatima.bishop46@inbox.example | Phoenix, AZ | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10720 | 2026-09-30 12:10 | soren.walker@webmail.example | Portland, OR | Smart Plug (2-Pack) ×1; Wool Throw Blanket ×1 | $93.00 | $0.00 | $93.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10721 | 2026-09-30 12:49 | lucas.young69@webmail.example | Baltimore, MD | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | RF-30143, INV-50027 | — |
| JL-10722 | 2026-09-30 17:07 | tamara.nguyen@mailbox.example | Los Angeles, CA | Wool Throw Blanket ×1; Bamboo Cutting Board ×1 | $92.00 | $0.00 | $92.00 | Mastercard | Standard | delivered | RT-20142, RF-30177 | — |
| JL-10723 | 2026-09-30 17:50 | liam.gupta55@webmail.example | Las Vegas, NV | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | WC-40067 | — |
| JL-10724 | 2026-09-30 19:23 | grace.daniels26@mailbox.example | Chicago, IL | Smart Plug (2-Pack) ×2 | $50.00 | $0.00 | $50.00 | PayPal | Standard | delivered | RT-20134, RF-30169 | — |
| JL-10725 | 2026-09-30 19:38 | owen.nelson@inbox.example | Milwaukee, WI | Cast Iron Skillet ×3; Adjustable Phone Stand ×1 | $180.00 | $0.00 | $180.00 | Visa | Standard | delivered | — | — |
| JL-10726 | 2026-10-01 00:32 | aaliyah.singh@webmail.example | Portland, ME | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Juniper Lane gift card | Standard | delivered | RT-20138, RF-30181 | — |
| JL-10727 | 2026-10-01 11:52 | james.fischer@webmail.example | Nashville, TN | Wireless Earbuds Pro ×2 | $158.00 | $0.00 | $158.00 | Visa | Standard | delivered | WC-40059 | — |
| JL-10728 | 2026-10-01 13:20 | mei.daniels@inbox.example | Philadelphia, PA | Electric Kettle 1.7L ×1; Bamboo Cutting Board ×1 | $69.00 | $12.99 | $81.99 | Visa | Express | delivered | RT-20156 | — |
| JL-10729 | 2026-10-01 13:24 | nora.martinez@mailbox.example | Kansas City, MO | Linen Napkins (Set of 4) ×1; Wireless Earbuds Pro ×1; Ceramic Pour-Over Coffee Set ×1 | $139.50 | $0.00 | $139.50 | Mastercard | Standard | delivered | RT-20165, RF-30205 | — |
| JL-10730 | 2026-10-01 15:02 | omar.kelly90@mailbox.example | Minneapolis, MN | Personalised Leather Notebook ×1 (emboss "For Maya") | $29.00 | $4.99 | $33.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10731 | 2026-10-01 17:01 | owen.campbell69@webmail.example | Oklahoma City, OK | Personalised Leather Notebook ×1 (emboss "A. Rivera") | $29.00 | $4.99 | $33.99 | Mastercard | Standard | delivered | RT-20161, RF-30195 | — |
| JL-10732 | 2026-10-02 15:19 | tamara.singh@inbox.example | Oklahoma City, OK | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | — | — |
| JL-10733 | 2026-10-02 20:01 | brandon.walsh@webmail.example | New York, NY | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | PayPal | Express | delivered | RT-20186 | Delivered after estimated window |
| JL-10734 | 2026-10-02 23:38 | brandon.yamamoto26@mailbox.example | San Diego, CA | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | PayPal | Standard | delivered | — | — |
| JL-10735 | 2026-10-03 07:44 | marcus.fischer26@mailbox.example | Boise, ID | Electric Kettle 1.7L ×1; Smart Plug (2-Pack) ×1; Oak Side Table ×1 | $199.00 | $0.00 | $199.00 | Juniper Lane gift card | Standard | delivered | WC-40072 | Delivered after estimated window |
| JL-10736 | 2026-10-03 09:34 | noah.reyes60@webmail.example | Burlington, VT | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10737 | 2026-10-03 09:41 | hazel.jackson8@webmail.example | Providence, RI | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | Visa | Standard | delivered | — | — |
| JL-10738 | 2026-10-03 14:32 | lily.jackson48@mailbox.example | Atlanta, GA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | cancelled | RF-30135 | Cancelled 2026-10-04 11:25: Customer request — ordered wrong item |
| JL-10739 | 2026-10-03 16:08 | aaliyah.brooks@inbox.example | San Francisco, CA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | RF-30152, DMG-55008 | — |
| JL-10740 | 2026-10-03 16:57 | tessa.edwards7@mailbox.example | Las Vegas, NV | Smart Plug (2-Pack) ×1; Linen Napkins (Set of 4) ×1 | $43.50 | $12.99 | $56.49 | Mastercard | Express | delivered | — | — |
| JL-10741 | 2026-10-04 07:43 | wyatt.sanders@mailbox.example | Albuquerque, NM | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | RF-30147, DMG-55009 | — |
| JL-10742 | 2026-10-04 11:17 | diego.fischer29@webmail.example | Cleveland, OH | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | RF-30157, DMG-55010 | — |
| JL-10743 | 2026-10-04 11:59 | james.foster@mailbox.example | Washington, DC | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Mastercard | Standard | delivered | — | — |
| JL-10744 | 2026-10-04 16:16 | gabriel.vasquez@webmail.example | Detroit, MI | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | delivered | — | — |
| JL-10745 | 2026-10-04 20:23 | keisha.hammond77@inbox.example | New York, NY | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | Mastercard | Standard | delivered | — | — |
| JL-10746 | 2026-10-05 08:48 | nora.larson39@inbox.example | Tampa, FL | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | — | — |
| JL-10747 | 2026-10-05 09:23 | hazel.quinn29@inbox.example | Omaha, NE | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | delivered | — | — |
| JL-10748 | 2026-10-05 09:51 | devon.lewis@webmail.example | Austin, TX | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | — | — |
| JL-10749 | 2026-10-05 10:52 | abigail.martinez@mailbox.example | Portland, ME | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | RT-20148, RF-30185 | — |
| JL-10750 | 2026-10-05 10:56 | lily.daniels@mailbox.example | Richmond, VA | Smart Plug (2-Pack) ×2 | $50.00 | $0.00 | $50.00 | PayPal | Standard | delivered | — | — |
| JL-10751 | 2026-10-05 14:32 | jamal.walsh96@inbox.example | Charlotte, NC | Ceramic Planter Set ×1; Linen Napkins (Set of 4) ×1 | $50.50 | $0.00 | $50.50 | Visa | Standard | delivered | — | — |
| JL-10752 | 2026-10-05 15:25 | hiro.walker@webmail.example | Columbus, OH | Wool Throw Blanket ×1; Scented Soy Candle ×1; Electric Kettle 1.7L ×2 | $170.00 | $0.00 | $170.00 | Mastercard | Standard | delivered | WC-40066 | — |
| JL-10753 | 2026-10-05 15:31 | soren.gupta28@webmail.example | Orlando, FL | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | American Express | Standard | delivered | WC-40060 | — |
| JL-10754 | 2026-10-05 15:48 | lucas.young69@webmail.example | Baltimore, MD | Personalised Leather Notebook ×1 (emboss "Mom") | $29.00 | $12.99 | $41.99 | Mastercard | Express | delivered | — | — |
| JL-10755 | 2026-10-05 16:18 | levi.singh53@mailbox.example | Raleigh, NC | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10756 | 2026-10-05 17:58 | zoey.sanders69@inbox.example | Washington, DC | Bamboo Cutting Board ×1; Electric Kettle 1.7L ×1 | $69.00 | $0.00 | $69.00 | PayPal | Standard | delivered | RF-30153, INV-50029 | — |
| JL-10757 | 2026-10-05 18:40 | arjun.petrov@inbox.example | Portland, ME | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | American Express | Email (digital) | delivered | — | — |
| JL-10758 | 2026-10-06 09:47 | gabriel.davis67@inbox.example | Portland, ME | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | lost | RF-30163, INV-50030 | — |
| JL-10759 | 2026-10-06 10:17 | isaac.petrov88@mailbox.example | Seattle, WA | Smart Plug (2-Pack) ×1; LED Desk Lamp ×1; Ceramic Pour-Over Coffee Set ×1 | $101.50 | $0.00 | $101.50 | Mastercard | Standard | delivered | RT-20145, RF-30178 | — |
| JL-10760 | 2026-10-06 10:51 | arjun.garcia91@inbox.example | Miami, FL | Scented Soy Candle ×1; Electric Kettle 1.7L ×2; Wool Throw Blanket ×1 | $170.00 | $12.99 | $182.99 | PayPal | Express | delivered | WC-40063 | — |
| JL-10761 | 2026-10-06 13:19 | sophia.ingram94@inbox.example | Pittsburgh, PA | Wireless Earbuds Pro ×1; LED Desk Lamp ×1 | $113.50 | $0.00 | $113.50 | Mastercard | Standard | delivered | — | — |
| JL-10762 | 2026-10-06 13:20 | scarlett.walker43@mailbox.example | Des Moines, IA | Wireless Earbuds Pro ×1; Adjustable Phone Stand ×1 | $94.00 | $12.99 | $106.99 | Mastercard | Express | delivered | — | — |
| JL-10763 | 2026-10-06 21:05 | julian.alvarez60@mailbox.example | Omaha, NE | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Visa | Express | delivered | RT-20139, RF-30171 | — |
| JL-10764 | 2026-10-07 07:42 | devon.gray17@inbox.example | Pittsburgh, PA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | RT-20166, RF-30202 | — |
| JL-10765 | 2026-10-07 10:27 | isabella.perry77@webmail.example | Albuquerque, NM | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | WC-40068 | — |
| JL-10766 | 2026-10-07 11:13 | harper.underwood@mailbox.example | Denver, CO | Wool Throw Blanket ×3; Bamboo Cutting Board ×1; Personalised Leather Notebook ×1 (emboss "Dad"); LED Desk Lamp ×1 | $291.50 | $0.00 | $291.50 | Mastercard | Standard | delivered | RT-20155, RF-30196 | — |
| JL-10767 | 2026-10-07 12:46 | priya.jensen@webmail.example | Cleveland, OH | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Visa | Standard | delivered | — | — |
| JL-10768 | 2026-10-07 13:15 | devon.thompson36@webmail.example | Dallas, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | cancelled | RF-30139 | Cancelled 2026-10-07 15:00: Customer request — found item elsewhere |
| JL-10769 | 2026-10-07 15:16 | henry.bennett@inbox.example | Raleigh, NC | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | Mastercard | Standard | delivered | — | — |
| JL-10770 | 2026-10-07 16:52 | ella.lopez55@mailbox.example | Phoenix, AZ | Scented Soy Candle ×2 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10771 | 2026-10-07 19:22 | owen.ortiz41@mailbox.example | Milwaukee, WI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10772 | 2026-10-08 12:56 | brandon.harris20@mailbox.example | Charlotte, NC | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | RT-20191 | — |
| JL-10773 | 2026-10-08 19:25 | ethan.thompson@mailbox.example | Anchorage, AK | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | lost | RF-30174, INV-50031 | — |
| JL-10774 | 2026-10-09 07:07 | soren.lopez88@webmail.example | Phoenix, AZ | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | Visa | Express | delivered | — | — |
| JL-10775 | 2026-10-09 08:11 | aiden.lewis@inbox.example | Des Moines, IA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | PayPal | Standard | delivered | — | — |
| JL-10776 | 2026-10-09 11:07 | ethan.daniels@inbox.example | Providence, RI | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Mastercard | Express | delivered | — | — |
| JL-10777 | 2026-10-09 11:26 | maya.lopez39@inbox.example | Honolulu, HI | Scented Soy Candle ×1; Electric Kettle 1.7L ×2 | $102.00 | $0.00 | $102.00 | PayPal | Standard | delivered | — | — |
| JL-10778 | 2026-10-09 16:11 | arjun.okafor@mailbox.example | Los Angeles, CA | Ceramic Planter Set ×1 | $32.00 | $12.99 | $44.99 | Mastercard | Express | delivered | RT-20167 | — |
| JL-10779 | 2026-10-09 16:14 | harper.reyes17@inbox.example | Orlando, FL | Linen Napkins (Set of 4) ×3 | $55.50 | $0.00 | $55.50 | Mastercard | Standard | delivered | — | — |
| JL-10780 | 2026-10-09 19:08 | diego.lopez@mailbox.example | Atlanta, GA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | RT-20162, RF-30207 | — |
| JL-10781 | 2026-10-09 19:41 | amelia.ellis@inbox.example | Kansas City, MO | Wireless Earbuds Pro ×1; Personalised Leather Notebook ×1 (emboss "J\&M 2026"); LED Desk Lamp ×1 | $142.50 | $0.00 | $142.50 | PayPal | Standard | delivered | — | — |
| JL-10782 | 2026-10-09 19:50 | dylan.daniels43@inbox.example | Oklahoma City, OK | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | American Express | Standard | delivered | — | — |
| JL-10783 | 2026-10-09 20:03 | ingrid.alvarez@mailbox.example | Baltimore, MD | Scented Soy Candle ×3; Bluetooth Speaker Mini ×1 | $75.99 | $0.00 | $75.99 | Visa | Standard | delivered | — | — |
| JL-10784 | 2026-10-09 22:40 | ava.turner67@webmail.example | Salt Lake City, UT | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | American Express | Standard | delivered | — | — |
| JL-10785 | 2026-10-10 09:19 | jamal.daniels54@inbox.example | Seattle, WA | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | American Express | Email (digital) | delivered | — | — |
| JL-10786 | 2026-10-10 10:05 | ella.vasquez@webmail.example | Raleigh, NC | Oak Side Table ×1; Scented Soy Candle ×1 | $141.00 | $0.00 | $141.00 | PayPal | Standard | delivered | — | — |
| JL-10787 | 2026-10-10 12:31 | mateo.singh@inbox.example | Austin, TX | Oak Side Table ×1 | $129.00 | $12.99 | $141.99 | Mastercard | Express | delivered | RT-20151, RF-30191 | — |
| JL-10788 | 2026-10-10 15:34 | arjun.morgan96@mailbox.example | Baltimore, MD | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Juniper Lane gift card | Standard | delivered | RT-20168, RF-30208 | — |
| JL-10789 | 2026-10-10 19:32 | keisha.morgan39@webmail.example | Salt Lake City, UT | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10790 | 2026-10-10 21:59 | lily.johnson@mailbox.example | Burlington, VT | Smart Plug (2-Pack) ×1; Adjustable Phone Stand ×1; Wireless Earbuds Pro ×3 | $277.00 | $0.00 | $277.00 | Visa | Standard | cancelled | RF-30144 | Cancelled 2026-10-10 23:22: Customer request — found item elsewhere |
| JL-10791 | 2026-10-11 09:59 | keisha.bennett@webmail.example | Tampa, FL | Wireless Earbuds Pro ×1; Bluetooth Speaker Mini ×1; Ceramic Planter Set ×2; Scented Soy Candle ×1 | $194.99 | $0.00 | $194.99 | PayPal | Standard | delivered | — | — |
| JL-10792 | 2026-10-11 11:06 | caleb.harris86@webmail.example | Burlington, VT | Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×2 | $104.98 | $0.00 | $104.98 | Visa | Standard | delivered | WC-40070 | — |
| JL-10793 | 2026-10-11 14:37 | aiden.novak@inbox.example | Indianapolis, IN | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | WC-40076 | — |
| JL-10794 | 2026-10-11 19:40 | harper.larson18@inbox.example | Kansas City, MO | Personalised Leather Notebook ×1 (emboss "Thank you, Ms. P") | $29.00 | $12.99 | $41.99 | Mastercard | Express | delivered | — | — |
| JL-10795 | 2026-10-12 02:08 | lucas.quinn@webmail.example | Raleigh, NC | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10796 | 2026-10-12 09:06 | logan.bennett18@inbox.example | New York, NY | Bamboo Cutting Board ×1; Smart Plug (2-Pack) ×1 | $49.00 | $4.99 | $53.99 | Mastercard | Standard | delivered | — | — |
| JL-10797 | 2026-10-12 09:24 | liam.bennett@webmail.example | Oklahoma City, OK | Bluetooth Speaker Mini ×2 | $79.98 | $0.00 | $79.98 | Visa | Standard | delivered | — | — |
| JL-10798 | 2026-10-12 12:21 | gabriel.hughes@webmail.example | Philadelphia, PA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | WC-40074 | — |
| JL-10799 | 2026-10-12 14:04 | elijah.quinn43@mailbox.example | Minneapolis, MN | Linen Napkins (Set of 4) ×1; Wireless Earbuds Pro ×1 | $97.50 | $0.00 | $97.50 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10800 | 2026-10-12 14:39 | olivia.sanders@webmail.example | Houston, TX | Adjustable Phone Stand ×1; Electric Kettle 1.7L ×2 | $105.00 | $12.99 | $117.99 | Visa | Express | delivered | RT-20171, RF-30206 | — |
| JL-10801 | 2026-10-12 15:21 | lily.davis54@webmail.example | Las Vegas, NV | LED Desk Lamp ×1; Scented Soy Candle ×1; Electric Kettle 1.7L ×1; Wool Throw Blanket ×1 | $159.50 | $12.99 | $172.49 | Mastercard | Express | delivered | RT-20143, RF-30186 | — |
| JL-10802 | 2026-10-12 15:29 | mei.edwards7@webmail.example | Orlando, FL | Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam") | $58.00 | $0.00 | $58.00 | Mastercard | Standard | delivered | — | — |
| JL-10803 | 2026-10-12 15:34 | levi.xu99@mailbox.example | Los Angeles, CA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10804 | 2026-10-12 16:08 | hiro.brooks62@mailbox.example | Austin, TX | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | American Express | Standard | delivered | — | Delivered after estimated window |
| JL-10805 | 2026-10-13 19:34 | jackson.larson68@webmail.example | Nashville, TN | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10806 | 2026-10-13 20:01 | zoey.ellis36@webmail.example | Providence, RI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10807 | 2026-10-14 03:35 | aria.johnson79@inbox.example | Seattle, WA | Scented Soy Candle ×1; Oak Side Table ×1 | $141.00 | $12.99 | $153.99 | American Express | Express | delivered | — | — |
| JL-10808 | 2026-10-14 13:23 | henry.yamamoto33@mailbox.example | San Diego, CA | Bluetooth Speaker Mini ×2 | $79.98 | $12.99 | $92.97 | American Express | Express | delivered | RT-20192 | — |
| JL-10809 | 2026-10-14 13:34 | keisha.ingram64@inbox.example | New York, NY | Juniper Lane Gift Card ×1 ($50.00 card) | $50.00 | $0.00 | $50.00 | Visa | Email (digital) | delivered | — | — |
| JL-10810 | 2026-10-14 19:21 | omar.johnson@inbox.example | Albuquerque, NM | Bluetooth Speaker Mini ×1; Electric Kettle 1.7L ×1 | $84.99 | $0.00 | $84.99 | Visa | Standard | delivered | INV-50033 | — |
| JL-10811 | 2026-10-14 20:38 | gabriel.morgan19@inbox.example | Providence, RI | Smart Plug (2-Pack) ×1; Electric Kettle 1.7L ×1 | $70.00 | $0.00 | $70.00 | Visa | Standard | delivered | — | — |
| JL-10812 | 2026-10-15 10:44 | zoey.ellis36@webmail.example | Providence, RI | Oak Side Table ×1; Scented Soy Candle ×2; Bluetooth Speaker Mini ×1 | $192.99 | $0.00 | $192.99 | PayPal | Standard | delivered | — | — |
| JL-10813 | 2026-10-15 11:42 | elijah.kowalski8@mailbox.example | Austin, TX | Scented Soy Candle ×1; Electric Kettle 1.7L ×1; Bamboo Cutting Board ×2 | $105.00 | $0.00 | $105.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10814 | 2026-10-15 11:45 | isaac.reyes@inbox.example | Salt Lake City, UT | Smart Plug (2-Pack) ×2; Wireless Earbuds Pro ×1; Cast Iron Skillet ×1 | $184.00 | $0.00 | $184.00 | Mastercard | Standard | delivered | — | — |
| JL-10815 | 2026-10-15 11:55 | julian.daniels@mailbox.example | Boise, ID | Scented Soy Candle ×1; LED Desk Lamp ×2; Wireless Earbuds Pro ×1 | $160.00 | $0.00 | $160.00 | Visa | Standard | delivered | — | — |
| JL-10816 | 2026-10-15 12:11 | amelia.jensen@webmail.example | Raleigh, NC | Wool Throw Blanket ×1; Wireless Earbuds Pro ×1 | $147.00 | $0.00 | $147.00 | Mastercard | Standard | delivered | WC-40069 | — |
| JL-10817 | 2026-10-15 13:43 | arjun.davis@webmail.example | Milwaukee, WI | Scented Soy Candle ×1; LED Desk Lamp ×1 | $46.50 | $12.99 | $59.49 | Mastercard | Express | delivered | — | — |
| JL-10818 | 2026-10-15 14:15 | grace.yamamoto20@inbox.example | Boise, ID | Ceramic Planter Set ×16 | $512.00 | $0.00 | $512.00 | American Express | Standard | cancelled | RF-30156 | Cancelled 2026-10-16 14:22: More than 10 units of one product; stock limited — support contacted customer first |
| JL-10819 | 2026-10-15 18:53 | logan.jensen@mailbox.example | Seattle, WA | Wool Throw Blanket ×1; Linen Napkins (Set of 4) ×1 | $86.50 | $0.00 | $86.50 | PayPal | Standard | delivered | RT-20180 | — |
| JL-10820 | 2026-10-15 20:35 | devon.ingram74@webmail.example | Phoenix, AZ | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | PayPal | Standard | delivered | RT-20177, RF-30209 | — |
| JL-10821 | 2026-10-16 05:26 | julian.underwood@webmail.example | Honolulu, HI | Ceramic Planter Set ×2; Wool Throw Blanket ×1 | $132.00 | $0.00 | $132.00 | Visa | Standard | delivered | RT-20193 | Delivered after estimated window |
| JL-10822 | 2026-10-16 08:12 | chloe.reyes@webmail.example | Des Moines, IA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | — | — |
| JL-10823 | 2026-10-16 17:26 | mateo.bishop@inbox.example | Houston, TX | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | cancelled | RF-30158 | Cancelled 2026-10-17 06:48: Customer request — duplicate order |
| JL-10824 | 2026-10-16 18:00 | mateo.patel@webmail.example | Chicago, IL | Cast Iron Skillet ×1; LED Desk Lamp ×1 | $89.50 | $0.00 | $89.50 | Mastercard | Standard | delivered | — | Delivered after estimated window |
| JL-10825 | 2026-10-17 07:04 | aria.alvarez62@webmail.example | Austin, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | — | — |
| JL-10826 | 2026-10-17 10:24 | sophia.patel66@inbox.example | Boston, MA | Scented Soy Candle ×2 | $24.00 | $4.99 | $28.99 | Visa | Standard | delivered | — | — |
| JL-10827 | 2026-10-17 11:15 | grace.walsh@webmail.example | Raleigh, NC | Adjustable Phone Stand ×1 | $15.00 | $12.99 | $27.99 | Mastercard | Express | delivered | RT-20160 | — |
| JL-10828 | 2026-10-17 11:23 | tamara.rossi@inbox.example | Austin, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | PayPal | Standard | delivered | — | — |
| JL-10829 | 2026-10-17 11:52 | hazel.jackson8@webmail.example | Providence, RI | Adjustable Phone Stand ×1 | $15.00 | $4.99 | $19.99 | PayPal | Standard | delivered | — | — |
| JL-10830 | 2026-10-17 13:48 | gabriel.nguyen@mailbox.example | Raleigh, NC | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10831 | 2026-10-17 20:59 | evelyn.sanders96@mailbox.example | Portland, OR | Linen Napkins (Set of 4) ×2 | $37.00 | $4.99 | $41.99 | Visa | Standard | delivered | — | — |
| JL-10832 | 2026-10-18 10:27 | james.thompson@mailbox.example | Milwaukee, WI | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | PayPal | Standard | delivered | RT-20169, RF-30215 | — |
| JL-10833 | 2026-10-18 10:52 | henry.anderson@inbox.example | Chicago, IL | Wool Throw Blanket ×1; Bamboo Cutting Board ×1 | $92.00 | $0.00 | $92.00 | Mastercard | Standard | delivered | — | — |
| JL-10834 | 2026-10-18 14:40 | zoey.hughes@webmail.example | Las Vegas, NV | Adjustable Phone Stand ×1; Scented Soy Candle ×1 | $27.00 | $4.99 | $31.99 | American Express | Standard | delivered | — | — |
| JL-10835 | 2026-10-18 18:08 | keisha.ellis46@mailbox.example | Portland, OR | Bluetooth Speaker Mini ×1; LED Desk Lamp ×1 | $74.49 | $0.00 | $74.49 | Mastercard | Standard | delivered | — | — |
| JL-10836 | 2026-10-18 19:48 | tamara.campbell@webmail.example | Oklahoma City, OK | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Mastercard | Express | delivered | RT-20190 | — |
| JL-10837 | 2026-10-18 19:56 | hiro.harris27@webmail.example | Des Moines, IA | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | delivered | WC-40077 | Delivered after estimated window |
| JL-10838 | 2026-10-19 07:51 | logan.donovan@inbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Electric Kettle 1.7L ×1; Linen Napkins (Set of 4) ×1 | $87.50 | $0.00 | $87.50 | Mastercard | Standard | cancelled | RF-30159 | Cancelled 2026-10-19 11:26: Customer request — changed mind |
| JL-10839 | 2026-10-19 09:13 | abigail.garcia76@inbox.example | Baltimore, MD | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10840 | 2026-10-19 12:15 | mia.jensen@inbox.example | Omaha, NE | Bamboo Cutting Board ×1 | $24.00 | $12.99 | $36.99 | Visa | Express | delivered | RF-30179, INV-50032 | — |
| JL-10841 | 2026-10-19 16:04 | aiden.martinez@inbox.example | Minneapolis, MN | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10842 | 2026-10-19 18:42 | elijah.walker@mailbox.example | Indianapolis, IN | Ceramic Pour-Over Coffee Set ×1; Bluetooth Speaker Mini ×2; Scented Soy Candle ×2 | $145.98 | $0.00 | $145.98 | PayPal | Standard | delivered | — | — |
| JL-10843 | 2026-10-20 16:38 | olivia.novak51@webmail.example | Chicago, IL | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10844 | 2026-10-20 17:32 | caleb.chen15@webmail.example | Minneapolis, MN | Ceramic Pour-Over Coffee Set ×1; Oak Side Table ×1; Bluetooth Speaker Mini ×1 | $210.99 | $0.00 | $210.99 | American Express | Standard | delivered | RT-20181 | — |
| JL-10845 | 2026-10-20 21:16 | maya.lewis97@mailbox.example | Seattle, WA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | Delivered after estimated window |
| JL-10846 | 2026-10-21 09:48 | lucas.zimmerman70@inbox.example | Denver, CO | Adjustable Phone Stand ×1; Wool Throw Blanket ×1; Personalised Leather Notebook ×1 (emboss "A. Rivera") | $112.00 | $0.00 | $112.00 | Mastercard | Standard | cancelled | RF-30161 | Cancelled 2026-10-21 17:48: Customer request — found item elsewhere |
| JL-10847 | 2026-10-21 11:23 | ava.morgan@mailbox.example | Oklahoma City, OK | Bluetooth Speaker Mini ×1; Smart Plug (2-Pack) ×1; Wireless Earbuds Pro ×1; Electric Kettle 1.7L ×1 | $188.99 | $0.00 | $188.99 | Mastercard | Standard | delivered | RT-20178, RF-30216 | — |
| JL-10848 | 2026-10-21 11:35 | elijah.jensen13@mailbox.example | Baltimore, MD | Wool Throw Blanket ×3; Wireless Earbuds Pro ×2; Bamboo Cutting Board ×1 | $386.00 | $0.00 | $386.00 | Visa | Standard | cancelled | RF-30162 | Cancelled 2026-10-21 14:43: Customer request — duplicate order |
| JL-10849 | 2026-10-21 14:44 | tamara.rossi@inbox.example | Austin, TX | Scented Soy Candle ×1; Bamboo Cutting Board ×1; Smart Plug (2-Pack) ×1 | $61.00 | $0.00 | $61.00 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10850 | 2026-10-21 23:15 | hiro.ramirez@webmail.example | Austin, TX | Scented Soy Candle ×1; Bamboo Cutting Board ×1 | $36.00 | $12.99 | $48.99 | American Express | Express | delivered | — | — |
| JL-10851 | 2026-10-21 23:45 | elijah.kim78@webmail.example | Tampa, FL | Linen Napkins (Set of 4) ×1; Wireless Earbuds Pro ×1 | $97.50 | $0.00 | $97.50 | American Express | Standard | delivered | — | — |
| JL-10852 | 2026-10-22 06:19 | hiro.rossi38@webmail.example | Miami, FL | Personalised Leather Notebook ×1 (emboss "Field Notes - LK"); Cast Iron Skillet ×2; Bluetooth Speaker Mini ×2 | $218.98 | $12.99 | $231.97 | PayPal | Express | delivered | — | Delivered after estimated window |
| JL-10853 | 2026-10-22 06:54 | amelia.edwards@inbox.example | Boise, ID | Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "Field Notes - LK"); Bamboo Cutting Board ×1 | $65.00 | $0.00 | $65.00 | Visa | Standard | delivered | RT-20182, RF-30210 | — |
| JL-10854 | 2026-10-22 13:01 | soren.foster9@mailbox.example | Oklahoma City, OK | Scented Soy Candle ×3 | $36.00 | $4.99 | $40.99 | PayPal | Standard | delivered | — | — |
| JL-10855 | 2026-10-22 19:02 | aiden.rossi20@inbox.example | Denver, CO | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | RT-20183 | — |
| JL-10856 | 2026-10-22 19:06 | liam.brooks94@mailbox.example | Burlington, VT | Cast Iron Skillet ×1; Adjustable Phone Stand ×1; Bamboo Cutting Board ×1 | $94.00 | $12.99 | $106.99 | Visa | Express | delivered | — | — |
| JL-10857 | 2026-10-22 20:20 | nathan.yamamoto@mailbox.example | Milwaukee, WI | Smart Plug (2-Pack) ×1; Personalised Leather Notebook ×1 (emboss "Dr. Okafor") | $54.00 | $12.99 | $66.99 | Visa | Express | delivered | — | — |
| JL-10858 | 2026-10-22 23:58 | levi.chen@inbox.example | Salt Lake City, UT | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | Visa | Email (digital) | delivered | — | — |
| JL-10859 | 2026-10-23 07:12 | hazel.anderson55@inbox.example | Washington, DC | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | — | — |
| JL-10860 | 2026-10-23 09:22 | scarlett.zimmerman@mailbox.example | Las Vegas, NV | Ceramic Planter Set ×1; Smart Plug (2-Pack) ×1; Linen Napkins (Set of 4) ×1 | $75.50 | $12.99 | $88.49 | PayPal | Express | delivered | RT-20187 | — |
| JL-10861 | 2026-10-23 10:57 | dylan.rossi45@webmail.example | Orlando, FL | Ceramic Pour-Over Coffee Set ×1; Wireless Earbuds Pro ×1 | $121.00 | $0.00 | $121.00 | American Express | Standard | delivered | WC-40078 | — |
| JL-10862 | 2026-10-23 13:46 | mei.yamamoto@webmail.example | Des Moines, IA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Juniper Lane gift card | Standard | cancelled | RF-30170 | Cancelled 2026-10-23 14:14: Customer request — duplicate order |
| JL-10863 | 2026-10-23 19:44 | aiden.ortiz33@inbox.example | Tampa, FL | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Visa | Standard | delivered | — | — |
| JL-10864 | 2026-10-23 21:35 | liam.gupta53@webmail.example | Austin, TX | Scented Soy Candle ×13 | $156.00 | $0.00 | $156.00 | Mastercard | Standard | cancelled | RF-30172 | Cancelled 2026-10-24 04:16: More than 10 units of one product; stock limited — support contacted customer first |
| JL-10865 | 2026-10-24 09:36 | fatima.donovan88@mailbox.example | New York, NY | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | PayPal | Standard | delivered | DMG-55011 | — |
| JL-10866 | 2026-10-24 11:32 | julian.owens9@mailbox.example | Chicago, IL | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10867 | 2026-10-24 12:38 | maya.walker@webmail.example | Honolulu, HI | Personalised Leather Notebook ×1 (emboss "Class of 2026"); Oak Side Table ×1 | $158.00 | $0.00 | $158.00 | Mastercard | Standard | delivered | RT-20188 | — |
| JL-10868 | 2026-10-24 13:04 | diego.sanders64@mailbox.example | Orlando, FL | Bamboo Cutting Board ×1 | $24.00 | $4.99 | $28.99 | Mastercard | Standard | delivered | — | — |
| JL-10869 | 2026-10-24 14:17 | aiden.bishop46@webmail.example | Houston, TX | Electric Kettle 1.7L ×2 | $90.00 | $0.00 | $90.00 | Visa | Standard | delivered | RT-20170, RF-30211 | — |
| JL-10870 | 2026-10-24 20:57 | ethan.gray82@inbox.example | Charlotte, NC | Wireless Earbuds Pro ×1; Scented Soy Candle ×1; Ceramic Planter Set ×1 | $123.00 | $12.99 | $135.99 | American Express | Express | delivered | WC-40079 | — |
| JL-10871 | 2026-10-24 22:15 | lucas.xu84@webmail.example | New Orleans, LA | Smart Plug (2-Pack) ×1 | $25.00 | $12.99 | $37.99 | Visa | Express | delivered | RT-20179, RF-30212 | — |
| JL-10872 | 2026-10-25 05:54 | olivia.perry@webmail.example | San Diego, CA | Ceramic Pour-Over Coffee Set ×1; LED Desk Lamp ×1 | $76.50 | $0.00 | $76.50 | PayPal | Standard | delivered | RT-20172, RF-30217 | — |
| JL-10873 | 2026-10-25 08:05 | wyatt.jensen@inbox.example | Washington, DC | Cast Iron Skillet ×3; Scented Soy Candle ×1; Personalised Leather Notebook ×1 (emboss "Happy Birthday Sam") | $206.00 | $12.99 | $218.99 | PayPal | Express | delivered | — | — |
| JL-10874 | 2026-10-25 13:53 | soren.perry93@webmail.example | Oklahoma City, OK | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | cancelled | RF-30173 | Cancelled 2026-10-26 04:27: Customer request — duplicate order |
| JL-10875 | 2026-10-25 15:01 | elijah.jensen@mailbox.example | Tampa, FL | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Mastercard | Standard | delivered | — | — |
| JL-10876 | 2026-10-25 15:47 | logan.bishop3@inbox.example | Providence, RI | Bluetooth Speaker Mini ×1; Bamboo Cutting Board ×1 | $63.99 | $0.00 | $63.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10877 | 2026-10-25 17:33 | ava.jensen@webmail.example | Detroit, MI | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10878 | 2026-10-26 07:46 | owen.reyes@inbox.example | San Francisco, CA | Cast Iron Skillet ×2; Electric Kettle 1.7L ×1 | $155.00 | $0.00 | $155.00 | Visa | Standard | delivered | — | — |
| JL-10879 | 2026-10-26 10:49 | mateo.anderson@inbox.example | Phoenix, AZ | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | delivered | RT-20163, RF-30203 | — |
| JL-10880 | 2026-10-26 18:29 | amelia.harris15@mailbox.example | Dallas, TX | Wireless Earbuds Pro ×1; Bamboo Cutting Board ×1 | $103.00 | $0.00 | $103.00 | American Express | Standard | delivered | — | — |
| JL-10881 | 2026-10-27 09:52 | mateo.donovan@inbox.example | Boise, ID | Electric Kettle 1.7L ×1 | $45.00 | $12.99 | $57.99 | Visa | Express | delivered | — | — |
| JL-10882 | 2026-10-27 10:03 | maya.alvarez96@webmail.example | Richmond, VA | Electric Kettle 1.7L ×1; Oak Side Table ×1 | $174.00 | $0.00 | $174.00 | Visa | Standard | delivered | — | — |
| JL-10883 | 2026-10-27 14:57 | james.gray@inbox.example | Baltimore, MD | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | delivered | — | — |
| JL-10884 | 2026-10-27 18:43 | emma.ramirez@mailbox.example | Salt Lake City, UT | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | PayPal | Standard | delivered | — | — |
| JL-10885 | 2026-10-27 19:01 | elijah.daniels@inbox.example | Buffalo, NY | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | American Express | Email (digital) | delivered | — | — |
| JL-10886 | 2026-10-27 19:24 | aiden.owens83@mailbox.example | Portland, OR | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10887 | 2026-10-27 20:41 | nora.martinez97@inbox.example | Detroit, MI | Smart Plug (2-Pack) ×1; Bamboo Cutting Board ×1 | $49.00 | $4.99 | $53.99 | Visa | Standard | delivered | RT-20173, RF-30218 | — |
| JL-10888 | 2026-10-28 08:15 | zoey.kowalski@inbox.example | Orlando, FL | Wireless Earbuds Pro ×1; Scented Soy Candle ×1 | $91.00 | $12.99 | $103.99 | Mastercard | Express | delivered | — | — |
| JL-10889 | 2026-10-28 14:18 | henry.singh32@inbox.example | New Orleans, LA | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | RT-20174 | — |
| JL-10890 | 2026-10-28 17:34 | tamara.walsh64@inbox.example | Providence, RI | Ceramic Pour-Over Coffee Set ×1; Ceramic Planter Set ×1 | $74.00 | $12.99 | $86.99 | Mastercard | Express | delivered | — | — |
| JL-10891 | 2026-10-28 17:57 | isaac.kelly7@webmail.example | New York, NY | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | Mastercard | Standard | delivered | — | — |
| JL-10892 | 2026-10-28 21:10 | mia.garcia64@inbox.example | Omaha, NE | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | PayPal | Standard | delivered | — | — |
| JL-10893 | 2026-10-29 10:57 | olivia.hughes22@webmail.example | San Francisco, CA | Cast Iron Skillet ×1; Smart Plug (2-Pack) ×2 | $105.00 | $0.00 | $105.00 | American Express | Standard | delivered | — | — |
| JL-10894 | 2026-10-29 21:03 | keisha.singh6@mailbox.example | Chicago, IL | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | delivered | — | — |
| JL-10895 | 2026-10-29 21:28 | lucia.yamamoto@webmail.example | Chicago, IL | Adjustable Phone Stand ×1; Cast Iron Skillet ×2 | $125.00 | $0.00 | $125.00 | Mastercard | Standard | delivered | — | — |
| JL-10896 | 2026-10-30 05:23 | fatima.foster63@webmail.example | Indianapolis, IN | Personalised Leather Notebook ×2 (emboss "Happy Birthday Sam"); Linen Napkins (Set of 4) ×1; Bluetooth Speaker Mini ×1 | $116.49 | $0.00 | $116.49 | Visa | Standard | delivered | — | — |
| JL-10897 | 2026-10-30 09:48 | priya.larson21@inbox.example | Washington, DC | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $12.99 | $54.99 | Visa | Express | delivered | — | — |
| JL-10898 | 2026-10-30 10:57 | hazel.quinn29@inbox.example | Omaha, NE | Electric Kettle 1.7L ×2; Bluetooth Speaker Mini ×1 | $129.99 | $12.99 | $142.98 | Juniper Lane gift card | Express | delivered | — | — |
| JL-10899 | 2026-10-30 12:26 | mason.singh95@inbox.example | Cleveland, OH | LED Desk Lamp ×1; Adjustable Phone Stand ×1; Ceramic Pour-Over Coffee Set ×1 | $91.50 | $0.00 | $91.50 | Juniper Lane gift card | Standard | delivered | RT-20195 | Delivered after estimated window |
| JL-10900 | 2026-10-30 14:21 | ethan.davis4@inbox.example | Miami, FL | Bluetooth Speaker Mini ×1 | $39.99 | $12.99 | $52.98 | Mastercard | Express | delivered | — | — |
| JL-10901 | 2026-10-30 15:31 | aria.singh81@webmail.example | New York, NY | Wireless Earbuds Pro ×2; Bamboo Cutting Board ×1 | $182.00 | $0.00 | $182.00 | Visa | Standard | delivered | — | — |
| JL-10902 | 2026-10-30 16:38 | james.owens@inbox.example | Washington, DC | Bamboo Cutting Board ×2; Linen Napkins (Set of 4) ×1 | $66.50 | $0.00 | $66.50 | Mastercard | Standard | delivered | RT-20184 | — |
| JL-10903 | 2026-10-30 17:27 | nathan.daniels@mailbox.example | Des Moines, IA | Oak Side Table ×1; Smart Plug (2-Pack) ×1 | $154.00 | $12.99 | $166.99 | American Express | Express | cancelled | RF-30187 | Cancelled 2026-10-31 14:38: Customer request — changed mind |
| JL-10904 | 2026-10-31 08:21 | mia.nguyen@mailbox.example | Indianapolis, IN | Scented Soy Candle ×1; Bamboo Cutting Board ×1 | $36.00 | $4.99 | $40.99 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10905 | 2026-10-31 09:34 | henry.harris@mailbox.example | Nashville, TN | Bamboo Cutting Board ×2; Wool Throw Blanket ×1 | $116.00 | $0.00 | $116.00 | Mastercard | Standard | delivered | — | — |
| JL-10906 | 2026-10-31 09:43 | marcus.kim1@mailbox.example | Atlanta, GA | Scented Soy Candle ×1; LED Desk Lamp ×1; Bluetooth Speaker Mini ×1 | $86.49 | $12.99 | $99.48 | Visa | Express | delivered | — | — |
| JL-10907 | 2026-10-31 11:38 | lucia.mitchell6@webmail.example | Baltimore, MD | Wireless Earbuds Pro ×1; Bamboo Cutting Board ×2 | $127.00 | $0.00 | $127.00 | Mastercard | Standard | delivered | INV-50035 | — |
| JL-10908 | 2026-10-31 20:01 | lily.thompson30@mailbox.example | New York, NY | LED Desk Lamp ×1; Bamboo Cutting Board ×1 | $58.50 | $0.00 | $58.50 | Visa | Standard | lost | RF-30204, INV-50036 | — |
| JL-10909 | 2026-10-31 22:39 | priya.xu38@mailbox.example | Portland, ME | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | delivered | — | — |
| JL-10910 | 2026-11-01 11:44 | ethan.flores40@inbox.example | Salt Lake City, UT | Bamboo Cutting Board ×1; Cast Iron Skillet ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | delivered | — | — |
| JL-10911 | 2026-11-01 16:16 | mei.larson@mailbox.example | Boise, ID | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | — | — |
| JL-10912 | 2026-11-02 04:43 | noah.carter12@inbox.example | Los Angeles, CA | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | delivered | RT-20198 | — |
| JL-10913 | 2026-11-02 09:59 | ethan.lopez97@mailbox.example | Oklahoma City, OK | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10914 | 2026-11-02 14:10 | tamara.kowalski@mailbox.example | Omaha, NE | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | American Express | Standard | delivered | — | — |
| JL-10915 | 2026-11-02 15:13 | aiden.vasquez@mailbox.example | New Orleans, LA | Electric Kettle 1.7L ×1; Ceramic Planter Set ×2; Smart Plug (2-Pack) ×3 | $184.00 | $0.00 | $184.00 | PayPal | Standard | delivered | — | — |
| JL-10916 | 2026-11-02 15:43 | abigail.underwood51@mailbox.example | Orlando, FL | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | American Express | Standard | delivered | RF-30199, DMG-55012 | — |
| JL-10917 | 2026-11-03 15:23 | mateo.owens60@webmail.example | Burlington, VT | Smart Plug (2-Pack) ×1; Cast Iron Skillet ×1 | $80.00 | $0.00 | $80.00 | PayPal | Standard | delivered | RT-20196 | — |
| JL-10918 | 2026-11-03 22:20 | isabella.campbell77@mailbox.example | San Francisco, CA | Linen Napkins (Set of 4) ×1; Smart Plug (2-Pack) ×1; LED Desk Lamp ×2; Ceramic Pour-Over Coffee Set ×1 | $154.50 | $0.00 | $154.50 | Visa | Standard | delivered | — | Delivered after estimated window |
| JL-10919 | 2026-11-04 09:22 | aria.anderson@inbox.example | New Orleans, LA | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | PayPal | Standard | delivered | — | — |
| JL-10920 | 2026-11-04 09:28 | olivia.jackson@inbox.example | Tampa, FL | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | cancelled | RF-30190 | Cancelled 2026-11-04 09:48: Customer request — found item elsewhere |
| JL-10921 | 2026-11-04 11:58 | julian.nguyen13@mailbox.example | Washington, DC | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10922 | 2026-11-04 12:43 | chloe.walsh21@mailbox.example | Detroit, MI | Scented Soy Candle ×1; Wool Throw Blanket ×1 | $80.00 | $12.99 | $92.99 | American Express | Express | delivered | — | — |
| JL-10923 | 2026-11-04 16:47 | liam.martinez64@mailbox.example | Milwaukee, WI | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Visa | Email (digital) | delivered | — | — |
| JL-10924 | 2026-11-04 19:37 | aiden.anderson82@inbox.example | Columbus, OH | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | — | — |
| JL-10925 | 2026-11-04 20:33 | lily.zimmerman50@webmail.example | Orlando, FL | Wireless Earbuds Pro ×1; Bluetooth Speaker Mini ×1 | $118.99 | $0.00 | $118.99 | Visa | Standard | delivered | — | — |
| JL-10926 | 2026-11-05 06:49 | ella.xu38@mailbox.example | New Orleans, LA | Electric Kettle 1.7L ×2; Linen Napkins (Set of 4) ×1 | $108.50 | $0.00 | $108.50 | Visa | Standard | delivered | — | — |
| JL-10927 | 2026-11-05 08:44 | mia.ellis78@webmail.example | Los Angeles, CA | Bluetooth Speaker Mini ×2 | $79.98 | $0.00 | $79.98 | Visa | Standard | cancelled | RF-30192 | Cancelled 2026-11-05 10:57: Customer request — found item elsewhere |
| JL-10928 | 2026-11-05 08:58 | nathan.kelly24@mailbox.example | Burlington, VT | Linen Napkins (Set of 4) ×3; Electric Kettle 1.7L ×3 | $190.50 | $0.00 | $190.50 | Visa | Standard | delivered | — | — |
| JL-10929 | 2026-11-05 09:45 | grace.novak@inbox.example | Denver, CO | Cast Iron Skillet ×1 | $55.00 | $12.99 | $67.99 | Mastercard | Express | delivered | — | — |
| JL-10930 | 2026-11-05 09:48 | amelia.bennett@inbox.example | Washington, DC | Personalised Leather Notebook ×1 (emboss "Dr. Okafor") | $29.00 | $4.99 | $33.99 | Mastercard | Standard | delivered | RT-20194 | — |
| JL-10931 | 2026-11-05 10:23 | tessa.kim10@mailbox.example | Denver, CO | Bamboo Cutting Board ×1; Cast Iron Skillet ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | delivered | — | — |
| JL-10932 | 2026-11-05 18:30 | logan.martinez87@inbox.example | Chicago, IL | Juniper Lane Gift Card ×1 ($100.00 card) | $100.00 | $0.00 | $100.00 | PayPal | Email (digital) | delivered | — | — |
| JL-10933 | 2026-11-05 22:51 | amelia.walker@mailbox.example | Philadelphia, PA | Oak Side Table ×1; Cast Iron Skillet ×1 | $184.00 | $12.99 | $196.99 | Mastercard | Express | delivered | INV-50034 | — |
| JL-10934 | 2026-11-06 00:17 | hiro.ellis@inbox.example | San Francisco, CA | Smart Plug (2-Pack) ×1; Oak Side Table ×1 | $154.00 | $0.00 | $154.00 | Mastercard | Standard | delivered | INV-50037 | — |
| JL-10935 | 2026-11-06 07:49 | hiro.chen@inbox.example | Detroit, MI | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | PayPal | Standard | delivered | — | — |
| JL-10936 | 2026-11-06 09:57 | emma.campbell8@inbox.example | Charlotte, NC | Bamboo Cutting Board ×1; Adjustable Phone Stand ×1; Bluetooth Speaker Mini ×1 | $78.99 | $0.00 | $78.99 | Mastercard | Standard | delivered | — | — |
| JL-10937 | 2026-11-06 12:37 | arjun.donovan@inbox.example | Denver, CO | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Visa | Standard | delivered | — | — |
| JL-10938 | 2026-11-06 14:48 | caleb.iyer69@mailbox.example | Denver, CO | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $12.99 | $54.99 | Mastercard | Express | delivered | — | — |
| JL-10939 | 2026-11-06 16:35 | gabriel.anderson@mailbox.example | Oklahoma City, OK | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Visa | Standard | delivered | — | — |
| JL-10940 | 2026-11-06 17:23 | aaliyah.gupta31@webmail.example | Louisville, KY | Electric Kettle 1.7L ×2; Adjustable Phone Stand ×1 | $105.00 | $0.00 | $105.00 | Mastercard | Standard | delivered | — | — |
| JL-10941 | 2026-11-06 20:47 | diego.turner@mailbox.example | Cleveland, OH | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | cancelled | RF-30193 | Cancelled 2026-11-07 21:32: Customer request — duplicate order |
| JL-10942 | 2026-11-07 11:31 | grace.ellis@webmail.example | Miami, FL | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | Mastercard | Express | delivered | RT-20199 | — |
| JL-10943 | 2026-11-07 12:32 | chloe.foster7@mailbox.example | Providence, RI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | delivered | — | — |
| JL-10944 | 2026-11-07 15:19 | jackson.hughes28@inbox.example | Anchorage, AK | Smart Plug (2-Pack) ×1; Adjustable Phone Stand ×2 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | — | — |
| JL-10945 | 2026-11-07 19:59 | mei.walsh@webmail.example | New York, NY | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | PayPal | Standard | delivered | — | — |
| JL-10946 | 2026-11-07 20:27 | jamal.nguyen@inbox.example | Anchorage, AK | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | Visa | Standard | delivered | — | — |
| JL-10947 | 2026-11-08 12:42 | olivia.yamamoto@mailbox.example | New Orleans, LA | Ceramic Planter Set ×1 | $32.00 | $4.99 | $36.99 | Mastercard | Standard | delivered | — | — |
| JL-10948 | 2026-11-08 13:09 | noah.kelly@webmail.example | Cleveland, OH | Smart Plug (2-Pack) ×1 | $25.00 | $12.99 | $37.99 | Mastercard | Express | delivered | — | Delivered after estimated window |
| JL-10949 | 2026-11-08 13:31 | maya.walker@webmail.example | Honolulu, HI | Scented Soy Candle ×3; Electric Kettle 1.7L ×1 | $81.00 | $0.00 | $81.00 | PayPal | Standard | delivered | — | — |
| JL-10950 | 2026-11-08 21:22 | diego.garcia@inbox.example | Houston, TX | Cast Iron Skillet ×1 | $55.00 | $0.00 | $55.00 | American Express | Standard | delivered | — | — |
| JL-10951 | 2026-11-09 11:33 | noah.johnson@webmail.example | Dallas, TX | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | PayPal | Standard | delivered | — | — |
| JL-10952 | 2026-11-09 12:37 | henry.donovan33@mailbox.example | Columbus, OH | Scented Soy Candle ×2; Bluetooth Speaker Mini ×3 | $143.97 | $0.00 | $143.97 | Juniper Lane gift card | Standard | delivered | — | — |
| JL-10953 | 2026-11-09 14:18 | wyatt.kelly@mailbox.example | Kansas City, MO | Ceramic Pour-Over Coffee Set ×1; Bamboo Cutting Board ×2 | $90.00 | $0.00 | $90.00 | Mastercard | Standard | delivered | RT-20200 | — |
| JL-10954 | 2026-11-09 14:18 | mason.larson24@mailbox.example | Oklahoma City, OK | Wireless Earbuds Pro ×1 | $79.00 | $12.99 | $91.99 | Mastercard | Express | delivered | — | — |
| JL-10955 | 2026-11-09 14:28 | james.underwood@inbox.example | Omaha, NE | Wireless Earbuds Pro ×1; Bamboo Cutting Board ×2 | $127.00 | $0.00 | $127.00 | Mastercard | Standard | delivered | — | — |
| JL-10956 | 2026-11-09 14:54 | noah.kowalski93@webmail.example | Phoenix, AZ | LED Desk Lamp ×2 | $69.00 | $0.00 | $69.00 | Mastercard | Standard | delivered | — | — |
| JL-10957 | 2026-11-09 19:14 | ava.alvarez@inbox.example | Nashville, TN | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | Visa | Standard | cancelled | RF-30197 | Cancelled 2026-11-10 10:44: Customer request — changed mind |
| JL-10958 | 2026-11-09 19:44 | amelia.chen40@inbox.example | Omaha, NE | Smart Plug (2-Pack) ×1; Ceramic Planter Set ×1 | $57.00 | $12.99 | $69.99 | Visa | Express | cancelled | RF-30198 | Cancelled 2026-11-10 05:45: Customer request — ordered wrong item |
| JL-10959 | 2026-11-09 19:52 | henry.vasquez@webmail.example | Honolulu, HI | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | delivered | — | — |
| JL-10960 | 2026-11-10 08:24 | devon.ingram@mailbox.example | Washington, DC | Wool Throw Blanket ×1; Smart Plug (2-Pack) ×1 | $93.00 | $0.00 | $93.00 | Visa | Standard | dispatched | — | Delivered after estimated window |
| JL-10961 | 2026-11-10 08:56 | chloe.davis@inbox.example | Charlotte, NC | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Mastercard | Standard | delivered | — | — |
| JL-10962 | 2026-11-10 21:28 | owen.reyes@mailbox.example | Indianapolis, IN | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10963 | 2026-11-11 12:39 | julian.kim48@inbox.example | Kansas City, MO | Wireless Earbuds Pro ×1; Bluetooth Speaker Mini ×2 | $158.98 | $0.00 | $158.98 | Visa | Standard | delivered | — | — |
| JL-10964 | 2026-11-11 21:44 | keisha.foster@mailbox.example | Baltimore, MD | Juniper Lane Gift Card ×2 ($100.00 card) | $200.00 | $0.00 | $200.00 | American Express | Email (digital) | delivered | — | — |
| JL-10965 | 2026-11-12 12:01 | noah.ingram@inbox.example | Philadelphia, PA | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | delivered | — | — |
| JL-10966 | 2026-11-12 19:31 | james.turner58@mailbox.example | Baltimore, MD | Wool Throw Blanket ×2; Bluetooth Speaker Mini ×1 | $175.99 | $0.00 | $175.99 | Visa | Standard | delivered | — | — |
| JL-10967 | 2026-11-12 22:55 | wyatt.reyes21@inbox.example | Anchorage, AK | Linen Napkins (Set of 4) ×1 | $18.50 | $4.99 | $23.49 | PayPal | Standard | delivered | — | — |
| JL-10968 | 2026-11-13 09:34 | devon.underwood99@webmail.example | Providence, RI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Mastercard | Standard | dispatched | — | — |
| JL-10969 | 2026-11-13 15:17 | isaac.harris@mailbox.example | Indianapolis, IN | Wool Throw Blanket ×3 | $204.00 | $0.00 | $204.00 | PayPal | Standard | delivered | — | — |
| JL-10970 | 2026-11-13 15:20 | logan.sanders@webmail.example | Atlanta, GA | Wireless Earbuds Pro ×1; Smart Plug (2-Pack) ×1; Bluetooth Speaker Mini ×1 | $143.99 | $0.00 | $143.99 | Mastercard | Standard | delivered | — | — |
| JL-10971 | 2026-11-13 17:13 | liam.ortiz@inbox.example | Philadelphia, PA | Ceramic Pour-Over Coffee Set ×1 | $42.00 | $4.99 | $46.99 | Mastercard | Standard | dispatched | — | — |
| JL-10972 | 2026-11-13 18:44 | maya.davis74@inbox.example | Atlanta, GA | Scented Soy Candle ×1 | $12.00 | $12.99 | $24.99 | PayPal | Express | delivered | RT-20197 | — |
| JL-10973 | 2026-11-14 08:11 | nathan.bennett@inbox.example | Nashville, TN | Linen Napkins (Set of 4) ×2; Scented Soy Candle ×2 | $61.00 | $0.00 | $61.00 | Visa | Standard | dispatched | — | — |
| JL-10974 | 2026-11-14 12:26 | harper.kelly28@inbox.example | Salt Lake City, UT | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | dispatched | — | — |
| JL-10975 | 2026-11-14 14:01 | tessa.nelson42@inbox.example | Minneapolis, MN | Ceramic Planter Set ×1; Bluetooth Speaker Mini ×1 | $71.99 | $0.00 | $71.99 | Visa | Standard | cancelled | RF-30200 | Cancelled 2026-11-15 13:51: Customer request — found item elsewhere |
| JL-10976 | 2026-11-14 15:30 | ava.davis@mailbox.example | San Francisco, CA | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Visa | Standard | dispatched | — | — |
| JL-10977 | 2026-11-14 20:31 | evelyn.gupta@mailbox.example | New Orleans, LA | Smart Plug (2-Pack) ×2 | $50.00 | $0.00 | $50.00 | Visa | Standard | dispatched | — | — |
| JL-10978 | 2026-11-15 12:31 | nora.flores67@webmail.example | Burlington, VT | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | PayPal | Standard | dispatched | — | — |
| JL-10979 | 2026-11-15 12:53 | aria.chen@inbox.example | New Orleans, LA | Wireless Earbuds Pro ×2; Smart Plug (2-Pack) ×1 | $183.00 | $0.00 | $183.00 | American Express | Standard | dispatched | — | — |
| JL-10980 | 2026-11-15 20:30 | nora.novak@inbox.example | Providence, RI | Personalised Leather Notebook ×1 (emboss "J\&M 2026") | $29.00 | $4.99 | $33.99 | Mastercard | Standard | dispatched | — | — |
| JL-10981 | 2026-11-15 22:59 | aria.chen@webmail.example | Portland, ME | Wireless Earbuds Pro ×1; Oak Side Table ×1; Bluetooth Speaker Mini ×1; Scented Soy Candle ×1 | $259.99 | $0.00 | $259.99 | Mastercard | Standard | dispatched | — | — |
| JL-10982 | 2026-11-16 06:04 | noah.novak70@mailbox.example | Boise, ID | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | dispatched | — | — |
| JL-10983 | 2026-11-16 10:30 | dylan.garcia@webmail.example | Philadelphia, PA | Smart Plug (2-Pack) ×1 | $25.00 | $4.99 | $29.99 | PayPal | Standard | dispatched | — | — |
| JL-10984 | 2026-11-16 10:41 | diego.gupta@mailbox.example | Portland, ME | Electric Kettle 1.7L ×2 | $90.00 | $0.00 | $90.00 | PayPal | Standard | delivered | — | — |
| JL-10985 | 2026-11-16 21:24 | hiro.davis60@inbox.example | Boston, MA | Wool Throw Blanket ×1 | $68.00 | $0.00 | $68.00 | Visa | Standard | dispatched | — | Delivered after estimated window |
| JL-10986 | 2026-11-17 09:07 | soren.novak90@inbox.example | Omaha, NE | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | American Express | Standard | dispatched | — | Delivered after estimated window |
| JL-10987 | 2026-11-17 14:51 | chloe.underwood11@mailbox.example | San Francisco, CA | Wireless Earbuds Pro ×1; Ceramic Pour-Over Coffee Set ×2 | $163.00 | $12.99 | $175.99 | PayPal | Express | dispatched | — | — |
| JL-10988 | 2026-11-17 19:12 | evelyn.johnson37@webmail.example | Providence, RI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | dispatched | — | — |
| JL-10989 | 2026-11-17 23:12 | lucia.nguyen@mailbox.example | Charlotte, NC | Wireless Earbuds Pro ×1 | $79.00 | $0.00 | $79.00 | Juniper Lane gift card | Standard | dispatched | — | — |
| JL-10990 | 2026-11-18 12:13 | grace.bennett@inbox.example | Los Angeles, CA | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | PayPal | Standard | dispatched | — | — |
| JL-10991 | 2026-11-18 13:46 | priya.jensen@mailbox.example | Milwaukee, WI | Scented Soy Candle ×1 | $12.00 | $4.99 | $16.99 | Mastercard | Standard | dispatched | — | — |
| JL-10992 | 2026-11-18 19:56 | mia.rossi@mailbox.example | New York, NY | Bluetooth Speaker Mini ×1 | $39.99 | $4.99 | $44.98 | Visa | Standard | dispatched | — | — |
| JL-10993 | 2026-11-18 22:27 | henry.hammond95@inbox.example | Denver, CO | Juniper Lane Gift Card ×1 ($25.00 card) | $25.00 | $0.00 | $25.00 | Mastercard | Email (digital) | delivered | — | — |
| JL-10994 | 2026-11-19 09:11 | jackson.ortiz31@webmail.example | Houston, TX | Ceramic Planter Set ×1; Smart Plug (2-Pack) ×1 | $57.00 | $0.00 | $57.00 | Visa | Standard | dispatched | — | — |
| JL-10995 | 2026-11-19 10:36 | diego.ellis@inbox.example | Minneapolis, MN | Oak Side Table ×1; Wool Throw Blanket ×1 | $197.00 | $0.00 | $197.00 | Mastercard | Standard | dispatched | — | — |
| JL-10996 | 2026-11-19 11:44 | caleb.patel@inbox.example | Charlotte, NC | Linen Napkins (Set of 4) ×1; Personalised Leather Notebook ×1 (emboss "Happy Birthday Sam"); Electric Kettle 1.7L ×1 | $92.50 | $12.99 | $105.49 | Visa | Express | processing | — | — |
| JL-10997 | 2026-11-19 15:37 | maya.larson@mailbox.example | Milwaukee, WI | Electric Kettle 1.7L ×1 | $45.00 | $4.99 | $49.99 | Visa | Standard | processing | — | — |
| JL-10998 | 2026-11-19 18:54 | mia.singh@inbox.example | Austin, TX | LED Desk Lamp ×1 | $34.50 | $4.99 | $39.49 | Visa | Standard | cancelled | RF-30214 | Cancelled 2026-11-19 22:18: Customer request — changed mind |
| JL-10999 | 2026-11-19 19:56 | evelyn.ortiz15@webmail.example | Buffalo, NY | Scented Soy Candle ×1; Adjustable Phone Stand ×1; Linen Napkins (Set of 4) ×1 | $45.50 | $4.99 | $50.49 | Visa | Standard | processing | — | — |
| JL-11000 | 2026-11-19 21:48 | nathan.underwood41@inbox.example | Boston, MA | Oak Side Table ×1 | $129.00 | $0.00 | $129.00 | Visa | Standard | processing | — | — |
