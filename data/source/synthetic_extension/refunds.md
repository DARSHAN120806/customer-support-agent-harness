# Refunds: synthetic records

Imported from the extended knowledge base uploaded on 20 November 2026.
These records are NOT searchable by the assistant. scripts/import_synthetic_data.py turns them into data/orders.json and data/internal/.

> Everything below this line is generated test data. It is not real. All files in this pack share the same order IDs, dates and amounts. Data snapshot: **2026-11-20 09:00 ET**. Times are Eastern Time. Amounts are INR (Indian rupees).

## Refund ledger

Net = item refund + shipping refunded − return shipping fee − restocking fee. Orders paid with a gift card are refunded as store credit. Every refund was approved by a human support agent.

| Refund | Order ID | Email | Type | Item | Shipping refunded | Return fee | Restocking fee | Net refund | Refunded to | Approved by | Approved | Sent | Status | Reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RF-30001 | JL-10014 | priya.flores98@mailbox.example | Cancelled before dispatch | ₹12,400 | ₹0 | ₹0 | ₹0 | ₹12,400 | Original payment (Mastercard) | Dan K. | 2026-06-03 | 2026-06-04 | Sent | Cancellation |
| RF-30002 | JL-10020 | devon.johnson87@mailbox.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Dan K. | 2026-06-03 | 2026-06-08 | Sent | Cancellation |
| RF-30003 | JL-10032 | jamal.harris@inbox.example | Cancelled before dispatch | ₹4,200 | ₹499 | ₹0 | ₹0 | ₹4,699 | Original payment (Mastercard) | Sofia L. | 2026-06-05 | 2026-06-09 | Sent | Cancellation |
| RF-30004 | JL-10055 | tessa.quinn@mailbox.example | Cancelled before dispatch | ₹1,200 | ₹1,299 | ₹0 | ₹0 | ₹2,499 | Original payment (Visa) | Marcus T. | 2026-06-08 | 2026-06-10 | Sent | Cancellation |
| RF-30005 | JL-10068 | chloe.gupta75@mailbox.example | Cancelled before dispatch | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (PayPal) | Sofia L. | 2026-06-11 | 2026-06-12 | Sent | Cancellation |
| RF-30006 | JL-10096 | tessa.zimmerman@mailbox.example | Cancelled before dispatch | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (American Express) | Elena R. | 2026-06-15 | 2026-06-17 | Sent | Cancellation |
| RF-30007 | JL-10106 | isaac.petrov@mailbox.example | Cancelled before dispatch | ₹4,200 | ₹1,299 | ₹0 | ₹0 | ₹5,499 | Original payment (Mastercard) | Marcus T. | 2026-06-16 | 2026-06-17 | Sent | Cancellation |
| RF-30008 | JL-10104 | caleb.hammond80@webmail.example | Cancelled before dispatch | ₹6,350 | ₹0 | ₹0 | ₹0 | ₹6,350 | Original payment (Mastercard) | Sofia L. | 2026-06-17 | 2026-06-22 | Sent | Cancellation |
| RF-30009 | JL-10058 | noah.jensen@mailbox.example | Package confirmed lost / not received | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Sofia L. | 2026-06-23 | 2026-07-01 | Sent | INV-50001 |
| RF-30010 | JL-10071 | aiden.gray47@mailbox.example | Damaged on arrival | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (PayPal) | Sofia L. | 2026-06-23 | 2026-06-30 | Sent | DMG-55001 |
| RF-30011 | JL-10149 | mei.larson@mailbox.example | Cancelled before dispatch | ₹5,499 | ₹0 | ₹0 | ₹0 | ₹5,499 | Original payment (Visa) | Marcus T. | 2026-06-26 | 2026-07-01 | Sent | Cancellation |
| RF-30012 | JL-10064 | tessa.quinn@mailbox.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹500 | ₹1,301 | Original payment (Visa) | Dan K. | 2026-06-30 | 2026-07-09 | Sent | RT-20003 |
| RF-30013 | JL-10127 | maya.bennett@mailbox.example | Damaged on arrival | ₹1,200 | ₹1,299 | ₹0 | ₹0 | ₹2,499 | Original payment (Mastercard) | Elena R. | 2026-06-30 | 2026-07-09 | Sent | DMG-55002 |
| RF-30014 | JL-10093 | evelyn.johnson33@inbox.example | Package confirmed lost / not received | ₹3,450 | ₹1,299 | ₹0 | ₹0 | ₹4,749 | Original payment (Mastercard) | Marcus T. | 2026-07-01 | 2026-07-09 | Sent | INV-50004 |
| RF-30015 | JL-10211 | soren.alvarez@inbox.example | Cancelled before dispatch | ₹24,400 | ₹0 | ₹0 | ₹0 | ₹24,400 | Original payment (Visa) | Marcus T. | 2026-07-06 | 2026-07-07 | Sent | Cancellation |
| RF-30016 | JL-10026 | lucia.petrov51@mailbox.example | Return — change of mind | ₹1,500 | ₹0 | ₹699 | ₹0 | ₹801 | Original payment (Visa) | Dan K. | 2026-07-06 | 2026-07-14 | Sent | RT-20005 |
| RF-30017 | JL-10214 | abigail.morgan86@webmail.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Sofia L. | 2026-07-07 | 2026-07-08 | Sent | Cancellation |
| RF-30018 | JL-10215 | fatima.anderson@mailbox.example | Cancelled before dispatch | ₹8,000 | ₹0 | ₹0 | ₹0 | ₹8,000 | Original payment (Mastercard) | Elena R. | 2026-07-07 | 2026-07-08 | Sent | Cancellation |
| RF-30019 | JL-10040 | amelia.daniels94@mailbox.example | Return — faulty | ₹4,500 | ₹499 | ₹0 | ₹0 | ₹4,999 | Original payment (Visa) | Priya N. | 2026-07-07 | 2026-07-16 | Sent | RT-20006 |
| RF-30020 | JL-10072 | mia.gupta@inbox.example | Return — change of mind | ₹5,550 | ₹0 | ₹699 | ₹0 | ₹4,851 | Store credit | Sofia L. | 2026-07-07 | 2026-07-16 | Sent | RT-20004 |
| RF-30021 | JL-10246 | evelyn.gray92@mailbox.example | Cancelled before dispatch | ₹14,700 | ₹0 | ₹0 | ₹0 | ₹14,700 | Original payment (Mastercard) | Dan K. | 2026-07-12 | 2026-07-14 | Sent | Cancellation |
| RF-30022 | JL-10035 | aaliyah.ortiz@webmail.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Mastercard) | Sofia L. | 2026-07-14 | 2026-07-22 | Sent | RT-20008 |
| RF-30023 | JL-10268 | aiden.jackson@webmail.example | Cancelled before dispatch | ₹7,900 | ₹1,299 | ₹0 | ₹0 | ₹9,199 | Original payment (American Express) | Elena R. | 2026-07-16 | 2026-07-20 | Sent | Cancellation |
| RF-30024 | JL-10128 | mei.zimmerman@webmail.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Visa) | Sofia L. | 2026-07-16 | 2026-07-27 | Sent | RT-20007 |
| RF-30025 | JL-10080 | emma.flores@mailbox.example | Return — change of mind | ₹8,400 | ₹0 | ₹699 | ₹0 | ₹7,701 | Original payment (Visa) | Priya N. | 2026-07-17 | 2026-07-27 | Sent | RT-20009 |
| RF-30026 | JL-10281 | chloe.perry@webmail.example | Cancelled before dispatch | ₹4,500 | ₹499 | ₹0 | ₹0 | ₹4,999 | Original payment (Visa) | Elena R. | 2026-07-19 | 2026-07-20 | Sent | Cancellation |
| RF-30027 | JL-10291 | brandon.kim15@webmail.example | Cancelled before dispatch | ₹11,350 | ₹0 | ₹0 | ₹0 | ₹11,350 | Original payment (Visa) | Elena R. | 2026-07-19 | 2026-07-20 | Sent | Cancellation |
| RF-30028 | JL-10033 | ella.donovan60@mailbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Mastercard) | Dan K. | 2026-07-20 | 2026-07-28 | Sent | RT-20011 |
| RF-30029 | JL-10062 | caleb.edwards@webmail.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Original payment (Mastercard) | Marcus T. | 2026-07-20 | 2026-07-29 | Sent | RT-20018 |
| RF-30030 | JL-10299 | soren.carter@mailbox.example | Cancelled before dispatch | ₹2,400 | ₹1,299 | ₹0 | ₹0 | ₹3,699 | Original payment (Mastercard) | Dan K. | 2026-07-21 | 2026-07-23 | Sent | Cancellation |
| RF-30031 | JL-10304 | tessa.edwards1@webmail.example | Cancelled before dispatch | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (Visa) | Dan K. | 2026-07-22 | 2026-07-24 | Sent | Cancellation |
| RF-30032 | JL-10309 | ingrid.anderson40@mailbox.example | Cancelled before dispatch | ₹6,800 | ₹0 | ₹0 | ₹0 | ₹6,800 | Original payment (PayPal) | Elena R. | 2026-07-22 | 2026-07-27 | Sent | Cancellation |
| RF-30033 | JL-10223 | jamal.reyes55@inbox.example | Package confirmed lost / not received | ₹1,200 | ₹499 | ₹0 | ₹0 | ₹1,699 | Original payment (PayPal) | Dan K. | 2026-07-22 | 2026-07-29 | Sent | INV-50006 |
| RF-30034 | JL-10030 | ethan.turner96@mailbox.example | Return — change of mind | ₹1,500 | ₹0 | ₹699 | ₹225 | ₹576 | Original payment (Mastercard) | Dan K. | 2026-07-22 | 2026-07-30 | Sent | RT-20010 |
| RF-30035 | JL-10137 | liam.nelson11@webmail.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (Visa) | Marcus T. | 2026-07-23 | 2026-07-31 | Sent | RT-20012 |
| RF-30036 | JL-10130 | ava.campbell@webmail.example | Return — change of mind | ₹1,850 | ₹0 | ₹699 | ₹0 | ₹1,151 | Original payment (Visa) | Marcus T. | 2026-07-24 | 2026-08-04 | Sent | RT-20016 |
| RF-30037 | JL-10190 | jamal.harris@inbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (American Express) | Elena R. | 2026-07-24 | 2026-08-03 | Sent | RT-20020 |
| RF-30038 | JL-10323 | levi.chen@inbox.example | Cancelled before dispatch | ₹10,400 | ₹0 | ₹0 | ₹0 | ₹10,400 | Original payment (Mastercard) | Sofia L. | 2026-07-25 | 2026-07-28 | Sent | Cancellation |
| RF-30039 | JL-10243 | emma.ingram97@mailbox.example | Package confirmed lost / not received | ₹2,500 | ₹499 | ₹0 | ₹0 | ₹2,999 | Store credit | Sofia L. | 2026-07-27 | 2026-08-03 | Sent | INV-50007 |
| RF-30040 | JL-10162 | omar.daniels73@mailbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Visa) | Dan K. | 2026-07-27 | 2026-08-05 | Sent | RT-20019 |
| RF-30041 | JL-10110 | ethan.turner96@mailbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹825 | ₹3,976 | Original payment (PayPal) | Dan K. | 2026-07-28 | 2026-08-04 | Sent | RT-20014 |
| RF-30042 | JL-10148 | logan.ramirez@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Visa) | Priya N. | 2026-07-29 | 2026-08-06 | Sent | RT-20015 |
| RF-30043 | JL-10185 | rachel.hammond@mailbox.example | Return — change of mind | ₹13,600 | ₹0 | ₹699 | ₹0 | ₹12,901 | Original payment (American Express) | Priya N. | 2026-07-29 | 2026-08-07 | Sent | RT-20017 |
| RF-30044 | JL-10339 | scarlett.patel48@inbox.example | Cancelled before dispatch | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (Visa) | Dan K. | 2026-07-30 | 2026-08-04 | Sent | Cancellation |
| RF-30045 | JL-10221 | wyatt.jensen@inbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (PayPal) | Elena R. | 2026-07-30 | 2026-08-07 | Sent | RT-20030 |
| RF-30046 | JL-10239 | wyatt.patel27@webmail.example | Return — change of mind | ₹7,998 | ₹0 | ₹699 | ₹0 | ₹7,299 | Store credit | Dan K. | 2026-07-30 | 2026-08-10 | Sent | RT-20024 |
| RF-30047 | JL-10236 | mei.anderson@mailbox.example | Return — change of mind | ₹16,500 | ₹0 | ₹699 | ₹0 | ₹15,801 | Original payment (Visa) | Dan K. | 2026-07-31 | 2026-08-10 | Sent | RT-20021 |
| RF-30048 | JL-10176 | sophia.gray84@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (American Express) | Dan K. | 2026-08-03 | 2026-08-11 | Sent | RT-20022 |
| RF-30049 | JL-11009 | julian.johnson44@webmail.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (PayPal) | Marcus T. | 2026-08-04 | 2026-08-11 | Sent | RT-20034 |
| RF-30050 | JL-10131 | lily.zimmerman50@webmail.example | Return — faulty | ₹4,500 | ₹499 | ₹0 | ₹0 | ₹4,999 | Original payment (Mastercard) | Elena R. | 2026-08-05 | 2026-08-14 | Sent | RT-20027 |
| RF-30051 | JL-10168 | mason.gupta52@mailbox.example | Return — change of mind | ₹3,000 | ₹0 | ₹699 | ₹450 | ₹1,851 | Original payment (Mastercard) | Elena R. | 2026-08-05 | 2026-08-13 | Sent | RT-20023 |
| RF-30052 | JL-11012 | lucia.petrov51@mailbox.example | Return — faulty | ₹3,999 | ₹1,299 | ₹0 | ₹0 | ₹5,298 | Original payment (Visa) | Sofia L. | 2026-08-05 | 2026-08-12 | Sent | RT-20032 |
| RF-30053 | JL-10382 | lily.fischer@webmail.example | Cancelled before dispatch | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (Mastercard) | Marcus T. | 2026-08-06 | 2026-08-11 | Sent | Cancellation |
| RF-30054 | JL-10385 | logan.turner@webmail.example | Cancelled before dispatch | ₹16,599 | ₹0 | ₹0 | ₹0 | ₹16,599 | Original payment (Mastercard) | Priya N. | 2026-08-06 | 2026-08-11 | Sent | Cancellation |
| RF-30055 | JL-11005 | lily.jackson48@mailbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹0 | ₹3,501 | Original payment (Visa) | Sofia L. | 2026-08-06 | 2026-08-14 | Sent | RT-20033 |
| RF-30056 | JL-11016 | sophia.larson@webmail.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Visa) | Dan K. | 2026-08-06 | 2026-08-14 | Sent | RT-20028 |
| RF-30057 | JL-10270 | ingrid.kim57@inbox.example | Return — faulty | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Original payment (Mastercard) | Marcus T. | 2026-08-07 | 2026-08-18 | Sent | RT-20035 |
| RF-30058 | JL-10394 | elijah.ingram@webmail.example | Cancelled before dispatch | ₹5,700 | ₹0 | ₹0 | ₹0 | ₹5,700 | Original payment (Visa) | Elena R. | 2026-08-08 | 2026-08-12 | Sent | Cancellation |
| RF-30059 | JL-10140 | jackson.donovan@mailbox.example | Return — change of mind | ₹1,500 | ₹0 | ₹699 | ₹0 | ₹801 | Store credit | Dan K. | 2026-08-11 | 2026-08-19 | Sent | RT-20029 |
| RF-30060 | JL-10217 | owen.morgan@inbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (PayPal) | Priya N. | 2026-08-11 | 2026-08-18 | Sent | RT-20038 |
| RF-30061 | JL-10370 | sophia.patel@webmail.example | Damaged on arrival | ₹4,200 | ₹499 | ₹0 | ₹0 | ₹4,699 | Original payment (PayPal) | Dan K. | 2026-08-11 | 2026-08-20 | Sent | DMG-55004 |
| RF-30062 | JL-10431 | abigail.ellis51@webmail.example | Cancelled before dispatch | ₹24,000 | ₹0 | ₹0 | ₹0 | ₹24,000 | Original payment (Visa) | Elena R. | 2026-08-16 | 2026-08-17 | Sent | Cancellation |
| RF-30063 | JL-10202 | devon.fischer79@webmail.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (PayPal) | Dan K. | 2026-08-17 | 2026-08-26 | Sent | RT-20037 |
| RF-30064 | JL-10208 | aaliyah.edwards@inbox.example | Return — change of mind | ₹5,000 | ₹0 | ₹699 | ₹0 | ₹4,301 | Original payment (Mastercard) | Elena R. | 2026-08-17 | 2026-08-26 | Sent | RT-20045 |
| RF-30065 | JL-10249 | hiro.chen@inbox.example | Return — change of mind | ₹1,500 | ₹0 | ₹699 | ₹0 | ₹801 | Original payment (Visa) | Sofia L. | 2026-08-17 | 2026-08-24 | Sent | RT-20042 |
| RF-30066 | JL-10313 | harper.okafor37@webmail.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Mastercard) | Dan K. | 2026-08-17 | 2026-08-25 | Sent | RT-20044 |
| RF-30067 | JL-10269 | olivia.kelly@inbox.example | Return — change of mind | ₹11,997 | ₹0 | ₹699 | ₹0 | ₹11,298 | Original payment (PayPal) | Elena R. | 2026-08-18 | 2026-08-26 | Sent | RT-20047 |
| RF-30068 | JL-10287 | emma.ingram97@mailbox.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Mastercard) | Elena R. | 2026-08-18 | 2026-08-26 | Sent | RT-20046 |
| RF-30069 | JL-10461 | henry.hughes66@webmail.example | Cancelled before dispatch | ₹16,500 | ₹0 | ₹0 | ₹0 | ₹16,500 | Original payment (PayPal) | Dan K. | 2026-08-19 | 2026-08-24 | Sent | Cancellation |
| RF-30070 | JL-10172 | isaac.petrov88@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (PayPal) | Priya N. | 2026-08-19 | 2026-08-27 | Sent | RT-20041 |
| RF-30071 | JL-10258 | scarlett.bishop@mailbox.example | Return — faulty | ₹4,500 | ₹1,299 | ₹0 | ₹0 | ₹5,799 | Store credit | Marcus T. | 2026-08-19 | 2026-08-28 | Sent | RT-20039 |
| RF-30072 | JL-10263 | mia.alvarez@webmail.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹420 | ₹3,081 | Original payment (PayPal) | Elena R. | 2026-08-19 | 2026-08-26 | Sent | RT-20040 |
| RF-30073 | JL-10266 | emma.reyes97@mailbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹0 | ₹3,501 | Original payment (Visa) | Elena R. | 2026-08-19 | 2026-08-27 | Sent | RT-20048 |
| RF-30074 | JL-10332 | lucas.quinn@mailbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹0 | ₹3,501 | Original payment (Visa) | Sofia L. | 2026-08-20 | 2026-08-27 | Sent | RT-20052 |
| RF-30075 | JL-10484 | olivia.hughes41@inbox.example | Cancelled before dispatch | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (PayPal) | Dan K. | 2026-08-21 | 2026-08-25 | Sent | Cancellation |
| RF-30076 | JL-10481 | mason.turner9@inbox.example | Cancelled before dispatch | ₹7,998 | ₹0 | ₹0 | ₹0 | ₹7,998 | Original payment (PayPal) | Dan K. | 2026-08-22 | 2026-08-26 | Sent | Cancellation |
| RF-30077 | JL-10492 | soren.jackson@webmail.example | Cancelled before dispatch | ₹6,800 | ₹0 | ₹0 | ₹0 | ₹6,800 | Original payment (Mastercard) | Marcus T. | 2026-08-24 | 2026-08-26 | Sent | Cancellation |
| RF-30078 | JL-10395 | elijah.daniels@inbox.example | Package confirmed lost / not received | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (Visa) | Elena R. | 2026-08-25 | 2026-09-03 | Sent | INV-50013 |
| RF-30079 | JL-10401 | lily.underwood@inbox.example | Package confirmed lost / not received | ₹22,098 | ₹1,299 | ₹0 | ₹0 | ₹23,397 | Original payment (Visa) | Elena R. | 2026-08-25 | 2026-09-02 | Sent | INV-50014 |
| RF-30080 | JL-10310 | ingrid.gray@mailbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹420 | ₹3,081 | Original payment (Mastercard) | Sofia L. | 2026-08-25 | 2026-09-01 | Sent | RT-20049 |
| RF-30081 | JL-10343 | mason.singh47@mailbox.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (Visa) | Marcus T. | 2026-08-25 | 2026-09-02 | Sent | RT-20050 |
| RF-30082 | JL-10349 | hiro.ramirez27@inbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Visa) | Marcus T. | 2026-08-25 | 2026-09-03 | Sent | RT-20054 |
| RF-30083 | JL-10366 | jamal.thompson70@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Visa) | Priya N. | 2026-08-25 | 2026-09-03 | Sent | RT-20053 |
| RF-30084 | JL-10450 | mei.zimmerman@webmail.example | Package confirmed lost / not received | ₹12,900 | ₹0 | ₹0 | ₹0 | ₹12,900 | Original payment (Visa) | Dan K. | 2026-08-27 | 2026-09-04 | Sent | INV-50015 |
| RF-30085 | JL-11014 | julian.ramirez7@webmail.example | Return — faulty | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Original payment (Visa) | Dan K. | 2026-08-27 | 2026-09-03 | Sent | RT-20061 |
| RF-30086 | JL-10284 | mateo.perry@mailbox.example | Return — change of mind | ₹3,999 | ₹0 | ₹699 | ₹0 | ₹3,300 | Original payment (Visa) | Sofia L. | 2026-08-27 | 2026-09-04 | Sent | RT-20063 |
| RF-30087 | JL-10350 | maya.davis27@webmail.example | Return — faulty | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (American Express) | Elena R. | 2026-08-28 | 2026-09-09 | Sent | RT-20066 |
| RF-30088 | JL-10524 | levi.singh53@mailbox.example | Cancelled before dispatch | ₹6,400 | ₹0 | ₹0 | ₹0 | ₹6,400 | Original payment (Visa) | Priya N. | 2026-08-29 | 2026-09-01 | Sent | Cancellation |
| RF-30089 | JL-10331 | priya.owens@mailbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹900 | ₹2,901 | Original payment (Visa) | Priya N. | 2026-09-01 | 2026-09-10 | Sent | RT-20064 |
| RF-30090 | JL-10346 | scarlett.garcia45@webmail.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Original payment (PayPal) | Dan K. | 2026-09-01 | 2026-09-10 | Sent | RT-20059 |
| RF-30091 | JL-10377 | lucia.larson@webmail.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (Visa) | Elena R. | 2026-09-01 | 2026-09-11 | Sent | RT-20062 |
| RF-30092 | JL-10396 | hazel.hughes26@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Visa) | Elena R. | 2026-09-01 | 2026-09-11 | Sent | RT-20068 |
| RF-30093 | JL-10262 | soren.owens@inbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (Visa) | Elena R. | 2026-09-02 | 2026-09-10 | Sent | RT-20058 |
| RF-30094 | JL-10325 | jackson.daniels74@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹360 | ₹1,341 | Original payment (Mastercard) | Dan K. | 2026-09-02 | 2026-09-10 | Sent | RT-20074 |
| RF-30095 | JL-10375 | ava.hammond@mailbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Mastercard) | Sofia L. | 2026-09-02 | 2026-09-14 | Sent | RT-20057 |
| RF-30096 | JL-10379 | james.chen59@webmail.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Visa) | Dan K. | 2026-09-02 | 2026-09-11 | Sent | RT-20072 |
| RF-30097 | JL-10417 | arjun.rossi@inbox.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Original payment (Visa) | Marcus T. | 2026-09-02 | 2026-09-11 | Sent | RT-20069 |
| RF-30098 | JL-10391 | zoey.zimmerman@inbox.example | Return — change of mind | ₹12,900 | ₹0 | ₹699 | ₹2,580 | ₹9,621 | Original payment (Mastercard) | Sofia L. | 2026-09-04 | 2026-09-16 | Sent | RT-20070 |
| RF-30099 | JL-10507 | rachel.vasquez99@inbox.example | Damaged on arrival | ₹7,900 | ₹1,299 | ₹0 | ₹0 | ₹9,199 | Original payment (Visa) | Sofia L. | 2026-09-04 | 2026-09-14 | Sent | DMG-55006 |
| RF-30100 | JL-11013 | ella.harris81@webmail.example | Warranty — repair/replacement not possible | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Original payment (Mastercard) | Sofia L. | 2026-09-04 | 2026-09-15 | Sent | WC-40010 |
| RF-30101 | JL-10571 | diego.sanders64@mailbox.example | Cancelled before dispatch | ₹12,200 | ₹0 | ₹0 | ₹0 | ₹12,200 | Original payment (Visa) | Dan K. | 2026-09-06 | 2026-09-08 | Sent | Cancellation |
| RF-30102 | JL-10579 | tessa.mitchell81@inbox.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Dan K. | 2026-09-08 | 2026-09-11 | Sent | Cancellation |
| RF-30103 | JL-10404 | marcus.patel81@webmail.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (PayPal) | Marcus T. | 2026-09-08 | 2026-09-16 | Sent | RT-20071 |
| RF-30104 | JL-10448 | isaac.reyes50@inbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (PayPal) | Elena R. | 2026-09-08 | 2026-09-17 | Sent | RT-20082 |
| RF-30105 | JL-10473 | nathan.kelly@webmail.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Visa) | Marcus T. | 2026-09-08 | 2026-09-15 | Sent | RT-20083 |
| RF-30106 | JL-10442 | nora.okafor@webmail.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Visa) | Priya N. | 2026-09-09 | 2026-09-16 | Sent | RT-20073 |
| RF-30107 | JL-10436 | lucas.daniels3@webmail.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (PayPal) | Marcus T. | 2026-09-11 | 2026-09-18 | Sent | RT-20076 |
| RF-30108 | JL-10365 | tamara.bishop@webmail.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (PayPal) | Sofia L. | 2026-09-14 | 2026-09-22 | Sent | RT-20075 |
| RF-30109 | JL-10373 | isabella.vasquez43@mailbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Mastercard) | Sofia L. | 2026-09-14 | 2026-09-21 | Sent | RT-20085 |
| RF-30110 | JL-10399 | evelyn.sanders96@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (PayPal) | Dan K. | 2026-09-14 | 2026-09-22 | Sent | RT-20080 |
| RF-30111 | JL-10407 | scarlett.young@inbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (PayPal) | Dan K. | 2026-09-14 | 2026-09-22 | Sent | RT-20077 |
| RF-30112 | JL-10620 | scarlett.zimmerman@inbox.example | Cancelled before dispatch | ₹1,200 | ₹499 | ₹0 | ₹0 | ₹1,699 | Original payment (Visa) | Elena R. | 2026-09-15 | 2026-09-18 | Sent | Cancellation |
| RF-30113 | JL-10439 | wyatt.okafor@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Mastercard) | Dan K. | 2026-09-15 | 2026-09-22 | Sent | RT-20078 |
| RF-30114 | JL-10497 | ella.harris17@webmail.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Original payment (American Express) | Marcus T. | 2026-09-15 | 2026-09-22 | Sent | RT-20091 |
| RF-30115 | JL-10398 | omar.daniels73@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Mastercard) | Elena R. | 2026-09-16 | 2026-09-24 | Sent | RT-20089 |
| RF-30116 | JL-10478 | mason.iyer@webmail.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Visa) | Elena R. | 2026-09-16 | 2026-09-24 | Sent | RT-20088 |
| RF-30117 | JL-10663 | mason.novak49@webmail.example | Cancelled before dispatch | ₹1,200 | ₹499 | ₹0 | ₹0 | ₹1,699 | Original payment (PayPal) | Elena R. | 2026-09-20 | 2026-09-22 | Sent | Cancellation |
| RF-30118 | JL-10528 | owen.xu60@inbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Visa) | Sofia L. | 2026-09-21 | 2026-09-28 | Sent | RT-20094 |
| RF-30119 | JL-10420 | owen.sanders@mailbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Visa) | Priya N. | 2026-09-22 | 2026-09-30 | Sent | RT-20092 |
| RF-30120 | JL-10463 | evelyn.okafor78@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Store credit | Marcus T. | 2026-09-22 | 2026-09-29 | Sent | RT-20096 |
| RF-30121 | JL-10522 | evelyn.ellis@webmail.example | Return — change of mind | ₹12,900 | ₹0 | ₹699 | ₹0 | ₹12,201 | Original payment (Mastercard) | Dan K. | 2026-09-23 | 2026-10-01 | Sent | RT-20098 |
| RF-30122 | JL-10603 | arjun.petrov@webmail.example | Package confirmed lost / not received | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (PayPal) | Priya N. | 2026-09-25 | 2026-10-02 | Sent | INV-50018 |
| RF-30123 | JL-10440 | marcus.singh@webmail.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Mastercard) | Dan K. | 2026-09-25 | 2026-10-05 | Sent | RT-20103 |
| RF-30124 | JL-10552 | ingrid.nelson@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (American Express) | Priya N. | 2026-09-25 | 2026-10-02 | Sent | RT-20101 |
| RF-30125 | JL-10553 | caleb.kowalski@mailbox.example | Return — change of mind | ₹1,850 | ₹0 | ₹699 | ₹185 | ₹966 | Original payment (Mastercard) | Priya N. | 2026-09-25 | 2026-10-06 | Sent | RT-20106 |
| RF-30126 | JL-10709 | mia.turner52@inbox.example | Cancelled before dispatch | ₹6,499 | ₹0 | ₹0 | ₹0 | ₹6,499 | Original payment (Mastercard) | Priya N. | 2026-09-28 | 2026-09-29 | Sent | Cancellation |
| RF-30127 | JL-10710 | maya.ramirez@mailbox.example | Cancelled before dispatch | ₹5,050 | ₹0 | ₹0 | ₹0 | ₹5,050 | Store credit | Priya N. | 2026-09-28 | 2026-09-29 | Sent | Cancellation |
| RF-30128 | JL-10546 | ingrid.owens@inbox.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Mastercard) | Marcus T. | 2026-09-28 | 2026-10-06 | Sent | RT-20099 |
| RF-30129 | JL-10426 | scarlett.young@inbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹0 | ₹3,501 | Original payment (PayPal) | Sofia L. | 2026-09-29 | 2026-10-07 | Sent | RT-20102 |
| RF-30130 | JL-10433 | jamal.lopez@mailbox.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (Mastercard) | Priya N. | 2026-09-29 | 2026-10-07 | Sent | RT-20097 |
| RF-30131 | JL-10575 | mateo.ramirez90@mailbox.example | Return — change of mind | ₹8,400 | ₹0 | ₹699 | ₹0 | ₹7,701 | Original payment (PayPal) | Priya N. | 2026-09-29 | 2026-10-08 | Sent | RT-20100 |
| RF-30132 | JL-10596 | logan.thompson@inbox.example | Return — change of mind | ₹20,400 | ₹0 | ₹699 | ₹3,060 | ₹16,641 | Original payment (American Express) | Sofia L. | 2026-09-30 | 2026-10-09 | Sent | RT-20114 |
| RF-30133 | JL-10046 | grace.quinn@mailbox.example | Warranty — repair/replacement not possible | ₹23,700 | ₹0 | ₹0 | ₹0 | ₹23,700 | Original payment (Mastercard) | Marcus T. | 2026-10-01 | 2026-10-13 | Sent | WC-40020 |
| RF-30134 | JL-10501 | marcus.foster18@webmail.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Visa) | Elena R. | 2026-10-02 | 2026-10-14 | Sent | RT-20111 |
| RF-30135 | JL-10738 | lily.jackson48@mailbox.example | Cancelled before dispatch | ₹4,500 | ₹499 | ₹0 | ₹0 | ₹4,999 | Original payment (Visa) | Priya N. | 2026-10-04 | 2026-10-06 | Sent | Cancellation |
| RF-30136 | JL-10649 | chloe.quinn77@webmail.example | Package confirmed lost / not received | ₹4,500 | ₹499 | ₹0 | ₹0 | ₹4,999 | Original payment (Visa) | Sofia L. | 2026-10-06 | 2026-10-14 | Sent | INV-50023 |
| RF-30137 | JL-10537 | harper.walsh@webmail.example | Return — change of mind | ₹11,997 | ₹0 | ₹699 | ₹1,200 | ₹10,098 | Original payment (Visa) | Dan K. | 2026-10-06 | 2026-10-14 | Sent | RT-20112 |
| RF-30138 | JL-10602 | fatima.fischer69@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Visa) | Marcus T. | 2026-10-06 | 2026-10-14 | Sent | RT-20107 |
| RF-30139 | JL-10768 | devon.thompson36@webmail.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (PayPal) | Sofia L. | 2026-10-07 | 2026-10-13 | Sent | Cancellation |
| RF-30140 | JL-10583 | noah.foster48@inbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹1,580 | ₹5,621 | Original payment (Mastercard) | Sofia L. | 2026-10-07 | 2026-10-15 | Sent | RT-20115 |
| RF-30141 | JL-10435 | jamal.kim50@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Mastercard) | Elena R. | 2026-10-08 | 2026-10-20 | Sent | RT-20109 |
| RF-30142 | JL-10470 | elijah.carter@mailbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Visa) | Elena R. | 2026-10-08 | 2026-10-20 | Sent | RT-20110 |
| RF-30143 | JL-10721 | lucas.young69@webmail.example | Package confirmed lost / not received | ₹1,200 | ₹499 | ₹0 | ₹0 | ₹1,699 | Original payment (PayPal) | Marcus T. | 2026-10-09 | 2026-10-19 | Sent | INV-50027 |
| RF-30144 | JL-10790 | lily.johnson@mailbox.example | Cancelled before dispatch | ₹27,700 | ₹0 | ₹0 | ₹0 | ₹27,700 | Original payment (Visa) | Elena R. | 2026-10-10 | 2026-10-15 | Sent | Cancellation |
| RF-30145 | JL-10569 | nathan.perry@inbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Visa) | Elena R. | 2026-10-13 | 2026-10-21 | Sent | RT-20116 |
| RF-30146 | JL-10585 | caleb.lewis7@inbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹0 | ₹3,501 | Original payment (Visa) | Marcus T. | 2026-10-13 | 2026-10-20 | Sent | RT-20124 |
| RF-30147 | JL-10741 | wyatt.sanders@mailbox.example | Damaged on arrival | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (Visa) | Elena R. | 2026-10-13 | 2026-10-22 | Sent | DMG-55009 |
| RF-30148 | JL-10562 | omar.kelly90@mailbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (American Express) | Elena R. | 2026-10-14 | 2026-10-21 | Sent | RT-20113 |
| RF-30149 | JL-10648 | logan.sanders@webmail.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹500 | ₹1,301 | Original payment (PayPal) | Elena R. | 2026-10-14 | 2026-10-23 | Sent | RT-20117 |
| RF-30150 | JL-10683 | keisha.martinez9@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Mastercard) | Elena R. | 2026-10-14 | 2026-10-23 | Sent | RT-20127 |
| RF-30151 | JL-10690 | lucas.kim@webmail.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Store credit | Dan K. | 2026-10-14 | 2026-10-22 | Sent | RT-20122 |
| RF-30152 | JL-10739 | aaliyah.brooks@inbox.example | Damaged on arrival | ₹3,200 | ₹499 | ₹0 | ₹0 | ₹3,699 | Original payment (Visa) | Priya N. | 2026-10-14 | 2026-10-21 | Sent | DMG-55008 |
| RF-30153 | JL-10756 | zoey.sanders69@inbox.example | Package confirmed lost / not received | ₹6,900 | ₹0 | ₹0 | ₹0 | ₹6,900 | Original payment (PayPal) | Sofia L. | 2026-10-15 | 2026-10-26 | Sent | INV-50029 |
| RF-30154 | JL-10520 | mia.bennett34@webmail.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Mastercard) | Dan K. | 2026-10-15 | 2026-10-26 | Sent | RT-20119 |
| RF-30155 | JL-10622 | james.xu@webmail.example | Return — change of mind | ₹5,500 | ₹0 | ₹699 | ₹0 | ₹4,801 | Original payment (American Express) | Elena R. | 2026-10-15 | 2026-10-26 | Sent | RT-20129 |
| RF-30156 | JL-10818 | grace.yamamoto20@inbox.example | Cancelled before dispatch | ₹51,200 | ₹0 | ₹0 | ₹0 | ₹51,200 | Original payment (American Express) | Sofia L. | 2026-10-16 | 2026-10-19 | Sent | Cancellation |
| RF-30157 | JL-10742 | diego.fischer29@webmail.example | Damaged on arrival | ₹3,999 | ₹499 | ₹0 | ₹0 | ₹4,498 | Original payment (Visa) | Elena R. | 2026-10-16 | 2026-10-26 | Sent | DMG-55010 |
| RF-30158 | JL-10823 | mateo.bishop@inbox.example | Cancelled before dispatch | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (PayPal) | Priya N. | 2026-10-17 | 2026-10-21 | Sent | Cancellation |
| RF-30159 | JL-10838 | logan.donovan@inbox.example | Cancelled before dispatch | ₹8,750 | ₹0 | ₹0 | ₹0 | ₹8,750 | Original payment (Mastercard) | Priya N. | 2026-10-19 | 2026-10-22 | Sent | Cancellation |
| RF-30160 | JL-10679 | priya.quinn@inbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Mastercard) | Sofia L. | 2026-10-20 | 2026-10-29 | Sent | RT-20130 |
| RF-30161 | JL-10846 | lucas.zimmerman70@inbox.example | Cancelled before dispatch | ₹11,200 | ₹0 | ₹0 | ₹0 | ₹11,200 | Original payment (Mastercard) | Priya N. | 2026-10-21 | 2026-10-22 | Sent | Cancellation |
| RF-30162 | JL-10848 | elijah.jensen13@mailbox.example | Cancelled before dispatch | ₹38,600 | ₹0 | ₹0 | ₹0 | ₹38,600 | Original payment (Visa) | Dan K. | 2026-10-21 | 2026-10-22 | Sent | Cancellation |
| RF-30163 | JL-10758 | gabriel.davis67@inbox.example | Package confirmed lost / not received | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (Visa) | Dan K. | 2026-10-21 | 2026-10-30 | Sent | INV-50030 |
| RF-30164 | JL-10556 | aiden.lopez@inbox.example | Return — change of mind | ₹1,850 | ₹0 | ₹699 | ₹0 | ₹1,151 | Store credit | Marcus T. | 2026-10-21 | 2026-10-28 | Sent | RT-20125 |
| RF-30165 | JL-10616 | rachel.harris@webmail.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Mastercard) | Dan K. | 2026-10-21 | 2026-10-29 | Sent | RT-20131 |
| RF-30166 | JL-10643 | olivia.anderson52@mailbox.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Visa) | Dan K. | 2026-10-21 | 2026-10-28 | Sent | RT-20135 |
| RF-30167 | JL-10565 | lucas.nguyen@webmail.example | Return — faulty | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Store credit | Dan K. | 2026-10-22 | 2026-11-02 | Sent | RT-20136 |
| RF-30168 | JL-10592 | mason.daniels86@webmail.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹630 | ₹2,871 | Original payment (Visa) | Elena R. | 2026-10-22 | 2026-10-30 | Sent | RT-20126 |
| RF-30169 | JL-10724 | grace.daniels26@mailbox.example | Return — change of mind | ₹5,000 | ₹0 | ₹699 | ₹500 | ₹3,801 | Original payment (PayPal) | Elena R. | 2026-10-22 | 2026-11-02 | Sent | RT-20134 |
| RF-30170 | JL-10862 | mei.yamamoto@webmail.example | Cancelled before dispatch | ₹3,200 | ₹499 | ₹0 | ₹0 | ₹3,699 | Store credit | Sofia L. | 2026-10-23 | 2026-10-28 | Sent | Cancellation |
| RF-30171 | JL-10763 | julian.alvarez60@mailbox.example | Return — change of mind | ₹3,999 | ₹0 | ₹699 | ₹800 | ₹2,500 | Original payment (Visa) | Dan K. | 2026-10-23 | 2026-11-03 | Sent | RT-20139 |
| RF-30172 | JL-10864 | liam.gupta53@webmail.example | Cancelled before dispatch | ₹15,600 | ₹0 | ₹0 | ₹0 | ₹15,600 | Original payment (Mastercard) | Sofia L. | 2026-10-24 | 2026-10-26 | Sent | Cancellation |
| RF-30173 | JL-10874 | soren.perry93@webmail.example | Cancelled before dispatch | ₹3,999 | ₹499 | ₹0 | ₹0 | ₹4,498 | Original payment (Visa) | Sofia L. | 2026-10-26 | 2026-10-29 | Sent | Cancellation |
| RF-30174 | JL-10773 | ethan.thompson@mailbox.example | Package confirmed lost / not received | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Original payment (Visa) | Sofia L. | 2026-10-26 | 2026-11-02 | Sent | INV-50031 |
| RF-30175 | JL-10615 | arjun.martinez@inbox.example | Return — change of mind | ₹1,500 | ₹0 | ₹699 | ₹0 | ₹801 | Original payment (Visa) | Elena R. | 2026-10-26 | 2026-11-04 | Sent | RT-20132 |
| RF-30176 | JL-10647 | julian.petrov@mailbox.example | Return — change of mind | ₹6,400 | ₹0 | ₹699 | ₹1,280 | ₹4,421 | Original payment (Mastercard) | Elena R. | 2026-10-26 | 2026-11-02 | Sent | RT-20146 |
| RF-30177 | JL-10722 | tamara.nguyen@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Mastercard) | Priya N. | 2026-10-26 | 2026-11-02 | Sent | RT-20142 |
| RF-30178 | JL-10759 | isaac.petrov88@mailbox.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (Mastercard) | Dan K. | 2026-10-26 | 2026-11-02 | Sent | RT-20145 |
| RF-30179 | JL-10840 | mia.jensen@inbox.example | Package confirmed lost / not received | ₹2,400 | ₹1,299 | ₹0 | ₹0 | ₹3,699 | Original payment (Visa) | Sofia L. | 2026-10-27 | 2026-11-05 | Sent | INV-50032 |
| RF-30180 | JL-10696 | evelyn.okafor@inbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Visa) | Sofia L. | 2026-10-27 | 2026-11-04 | Sent | RT-20147 |
| RF-30181 | JL-10726 | aaliyah.singh@webmail.example | Return — change of mind | ₹3,999 | ₹0 | ₹699 | ₹0 | ₹3,300 | Store credit | Dan K. | 2026-10-27 | 2026-11-03 | Sent | RT-20138 |
| RF-30182 | JL-10708 | gabriel.johnson@mailbox.example | Return — change of mind | ₹1,200 | ₹0 | ₹699 | ₹0 | ₹501 | Original payment (Mastercard) | Sofia L. | 2026-10-28 | 2026-11-06 | Sent | RT-20141 |
| RF-30183 | JL-10676 | rachel.harris@webmail.example | Return — change of mind | ₹12,600 | ₹0 | ₹699 | ₹0 | ₹11,901 | Original payment (Mastercard) | Marcus T. | 2026-10-29 | 2026-11-09 | Sent | RT-20137 |
| RF-30184 | JL-10642 | dylan.edwards1@mailbox.example | Return — change of mind | ₹4,500 | ₹0 | ₹699 | ₹0 | ₹3,801 | Original payment (Visa) | Marcus T. | 2026-10-30 | 2026-11-10 | Sent | RT-20152 |
| RF-30185 | JL-10749 | abigail.martinez@mailbox.example | Return — wrong item received | ₹2,400 | ₹499 | ₹0 | ₹0 | ₹2,899 | Original payment (Mastercard) | Priya N. | 2026-10-30 | 2026-11-09 | Sent | RT-20148 |
| RF-30186 | JL-10801 | lily.davis54@webmail.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Mastercard) | Dan K. | 2026-10-30 | 2026-11-06 | Sent | RT-20143 |
| RF-30187 | JL-10903 | nathan.daniels@mailbox.example | Cancelled before dispatch | ₹15,400 | ₹1,299 | ₹0 | ₹0 | ₹16,699 | Original payment (American Express) | Marcus T. | 2026-10-31 | 2026-11-04 | Sent | Cancellation |
| RF-30188 | JL-10684 | abigail.larson@webmail.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹250 | ₹1,551 | Original payment (PayPal) | Sofia L. | 2026-11-02 | 2026-11-10 | Sent | RT-20140 |
| RF-30189 | JL-10479 | soren.mitchell@mailbox.example | Warranty — repair/replacement not possible | ₹15,800 | ₹0 | ₹0 | ₹0 | ₹15,800 | Original payment (PayPal) | Dan K. | 2026-11-02 | 2026-11-10 | Sent | WC-40045 |
| RF-30190 | JL-10920 | olivia.jackson@inbox.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Sofia L. | 2026-11-04 | 2026-11-09 | Sent | Cancellation |
| RF-30191 | JL-10787 | mateo.singh@inbox.example | Return — change of mind | ₹12,900 | ₹0 | ₹699 | ₹0 | ₹12,201 | Original payment (Mastercard) | Sofia L. | 2026-11-04 | 2026-11-13 | Sent | RT-20151 |
| RF-30192 | JL-10927 | mia.ellis78@webmail.example | Cancelled before dispatch | ₹7,998 | ₹0 | ₹0 | ₹0 | ₹7,998 | Original payment (Visa) | Sofia L. | 2026-11-05 | 2026-11-09 | Sent | Cancellation |
| RF-30193 | JL-10941 | diego.turner@mailbox.example | Cancelled before dispatch | ₹7,900 | ₹0 | ₹0 | ₹0 | ₹7,900 | Original payment (Visa) | Sofia L. | 2026-11-07 | 2026-11-12 | Sent | Cancellation |
| RF-30194 | JL-10701 | fatima.bennett@webmail.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Original payment (Visa) | Sofia L. | 2026-11-09 | 2026-11-19 | Sent | RT-20159 |
| RF-30195 | JL-10731 | owen.campbell69@webmail.example | Return — faulty | ₹2,900 | ₹499 | ₹0 | ₹0 | ₹3,399 | Original payment (Mastercard) | Elena R. | 2026-11-09 | 2026-11-17 | Sent | RT-20161 |
| RF-30196 | JL-10766 | harper.underwood@mailbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Mastercard) | Elena R. | 2026-11-09 | 2026-11-19 | Sent | RT-20155 |
| RF-30197 | JL-10957 | ava.alvarez@inbox.example | Cancelled before dispatch | ₹2,500 | ₹499 | ₹0 | ₹0 | ₹2,999 | Original payment (Visa) | Elena R. | 2026-11-10 | 2026-11-12 | Sent | Cancellation |
| RF-30198 | JL-10958 | amelia.chen40@inbox.example | Cancelled before dispatch | ₹5,700 | ₹1,299 | ₹0 | ₹0 | ₹6,999 | Original payment (Visa) | Dan K. | 2026-11-10 | 2026-11-13 | Sent | Cancellation |
| RF-30199 | JL-10916 | abigail.underwood51@mailbox.example | Damaged on arrival | ₹5,500 | ₹0 | ₹0 | ₹0 | ₹5,500 | Original payment (American Express) | Priya N. | 2026-11-12 | 2026-11-23 | Approved — payment pending | DMG-55012 |
| RF-30200 | JL-10975 | tessa.nelson42@inbox.example | Cancelled before dispatch | ₹7,199 | ₹0 | ₹0 | ₹0 | ₹7,199 | Original payment (Visa) | Marcus T. | 2026-11-15 | 2026-11-16 | Sent | Cancellation |
| RF-30201 | JL-10682 | keisha.ingram64@inbox.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (American Express) | Elena R. | 2026-11-16 | 2026-11-23 | Approved — payment pending | RT-20158 |
| RF-30202 | JL-10764 | devon.gray17@inbox.example | Return — change of mind | ₹3,999 | ₹0 | ₹699 | ₹0 | ₹3,300 | Original payment (Visa) | Elena R. | 2026-11-16 | 2026-11-23 | Approved — payment pending | RT-20166 |
| RF-30203 | JL-10879 | mateo.anderson@inbox.example | Return — change of mind | ₹6,800 | ₹0 | ₹699 | ₹0 | ₹6,101 | Original payment (Visa) | Elena R. | 2026-11-16 | 2026-11-23 | Approved — payment pending | RT-20163 |
| RF-30204 | JL-10908 | lily.thompson30@mailbox.example | Package confirmed lost / not received | ₹5,850 | ₹0 | ₹0 | ₹0 | ₹5,850 | Original payment (Visa) | Marcus T. | 2026-11-17 | 2026-11-24 | Approved — payment pending | INV-50036 |
| RF-30205 | JL-10729 | nora.martinez@mailbox.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹840 | ₹2,661 | Original payment (Mastercard) | Marcus T. | 2026-11-17 | 2026-11-24 | Approved — payment pending | RT-20165 |
| RF-30206 | JL-10800 | olivia.sanders@webmail.example | Return — change of mind | ₹9,000 | ₹0 | ₹699 | ₹0 | ₹8,301 | Original payment (Visa) | Priya N. | 2026-11-17 | 2026-11-25 | Approved — payment pending | RT-20171 |
| RF-30207 | JL-10780 | diego.lopez@mailbox.example | Return — change of mind | ₹3,450 | ₹0 | ₹699 | ₹0 | ₹2,751 | Original payment (Visa) | Marcus T. | 2026-11-18 | 2026-11-25 | Approved — payment pending | RT-20162 |
| RF-30208 | JL-10788 | arjun.morgan96@mailbox.example | Return — change of mind | ₹3,200 | ₹0 | ₹699 | ₹0 | ₹2,501 | Store credit | Dan K. | 2026-11-18 | 2026-11-27 | Approved — payment pending | RT-20168 |
| RF-30209 | JL-10820 | devon.ingram74@webmail.example | Return — change of mind | ₹3,999 | ₹0 | ₹699 | ₹0 | ₹3,300 | Original payment (PayPal) | Sofia L. | 2026-11-18 | 2026-11-30 | Approved — payment pending | RT-20177 |
| RF-30210 | JL-10853 | amelia.edwards@inbox.example | Return — change of mind | ₹2,400 | ₹0 | ₹699 | ₹0 | ₹1,701 | Original payment (Visa) | Priya N. | 2026-11-18 | 2026-11-25 | Approved — payment pending | RT-20182 |
| RF-30211 | JL-10869 | aiden.bishop46@webmail.example | Return — change of mind | ₹9,000 | ₹0 | ₹699 | ₹0 | ₹8,301 | Original payment (Visa) | Priya N. | 2026-11-18 | 2026-11-30 | Approved — payment pending | RT-20170 |
| RF-30212 | JL-10871 | lucas.xu84@webmail.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (Visa) | Marcus T. | 2026-11-18 | 2026-11-25 | Approved — payment pending | RT-20179 |
| RF-30213 | JL-10306 | chloe.bishop@webmail.example | Warranty — repair/replacement not possible | ₹4,500 | ₹0 | ₹0 | ₹0 | ₹4,500 | Original payment (Visa) | Sofia L. | 2026-11-18 | 2026-11-25 | Approved — payment pending | WC-40057 |
| RF-30214 | JL-10998 | mia.singh@inbox.example | Cancelled before dispatch | ₹3,450 | ₹499 | ₹0 | ₹0 | ₹3,949 | Original payment (Visa) | Elena R. | 2026-11-19 | 2026-11-20 | Approved — payment pending | Cancellation |
| RF-30215 | JL-10832 | james.thompson@mailbox.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (PayPal) | Priya N. | 2026-11-19 | 2026-11-27 | Approved — payment pending | RT-20169 |
| RF-30216 | JL-10847 | ava.morgan@mailbox.example | Return — change of mind | ₹7,900 | ₹0 | ₹699 | ₹0 | ₹7,201 | Original payment (Mastercard) | Sofia L. | 2026-11-19 | 2026-11-30 | Approved — payment pending | RT-20178 |
| RF-30217 | JL-10872 | olivia.perry@webmail.example | Return — change of mind | ₹4,200 | ₹0 | ₹699 | ₹420 | ₹3,081 | Original payment (PayPal) | Dan K. | 2026-11-19 | 2026-11-27 | Approved — payment pending | RT-20172 |
| RF-30218 | JL-10887 | nora.martinez97@inbox.example | Return — change of mind | ₹2,500 | ₹0 | ₹699 | ₹0 | ₹1,801 | Original payment (Visa) | Elena R. | 2026-11-19 | 2026-12-01 | Approved — payment pending | RT-20173 |

## Refund disputes

| Dispute | Refund | Order ID | Filed | Reason | Reviewed by | Decision date | Outcome | Additional refund |
|---|---|---|---|---|---|---|---|---|
| DS-70001 | RF-30012 | JL-10064 | 2026-07-11 | Item was returned in good condition | Helen W. (Senior) | 2026-07-14 | Fee waived | ₹500 |
| DS-70002 | RF-30034 | JL-10030 | 2026-08-02 | Item was returned in good condition | Helen W. (Senior) | 2026-08-04 | Fee waived | ₹225 |
| DS-70003 | RF-30041 | JL-10110 | 2026-08-05 | Item was returned in good condition | Helen W. (Senior) | 2026-08-07 | Upheld | — |
| DS-70004 | RF-30056 | JL-11016 | 2026-08-16 | Disagrees with ₹699 return shipping fee | Helen W. (Senior) | 2026-08-19 | Upheld | — |
| DS-70005 | RF-30089 | JL-10331 | 2026-09-13 | Item was returned in good condition | Helen W. (Senior) | 2026-09-14 | Fee reduced to 10% | ₹450 |
| DS-70006 | RF-30097 | JL-10417 | 2026-09-13 | Disagrees with ₹699 return shipping fee | Helen W. (Senior) | 2026-09-16 | Upheld | — |
| DS-70007 | RF-30094 | JL-10325 | 2026-09-14 | Item was returned in good condition | Helen W. (Senior) | 2026-09-15 | Fee reduced to 10% | ₹120 |
| DS-70008 | RF-30098 | JL-10391 | 2026-09-20 | Item was returned in good condition | Helen W. (Senior) | 2026-09-22 | Upheld | — |
| DS-70009 | RF-30125 | JL-10553 | 2026-10-08 | Item was returned in good condition | Helen W. (Senior) | 2026-10-13 | Upheld | — |
| DS-70010 | RF-30140 | JL-10583 | 2026-10-16 | Item was returned in good condition | Helen W. (Senior) | 2026-10-21 | Fee reduced to 10% | ₹790 |
| DS-70011 | RF-30149 | JL-10648 | 2026-10-24 | Item was returned in good condition | Helen W. (Senior) | 2026-10-27 | Fee waived | ₹500 |
| DS-70012 | RF-30145 | JL-10569 | 2026-10-25 | Disagrees with ₹699 return shipping fee | Helen W. (Senior) | 2026-10-27 | Upheld | — |
| DS-70013 | RF-30169 | JL-10724 | 2026-11-04 | Item was returned in good condition | Helen W. (Senior) | 2026-11-09 | Fee waived | ₹500 |
| DS-70014 | RF-30176 | JL-10647 | 2026-11-06 | Item was returned in good condition | Helen W. (Senior) | 2026-11-09 | Fee waived | ₹1,280 |
| DS-70015 | RF-30188 | JL-10684 | 2026-11-12 | Item was returned in good condition | Helen W. (Senior) | 2026-11-13 | Fee waived | ₹250 |

## Refund summary by type

| Type | Refunds | Total net |
|---|---|---|
| Cancelled before dispatch | 55 | ₹5,12,068 |
| Damaged on arrival | 8 | ₹36,942 |
| Package confirmed lost / not received | 15 | ₹93,088 |
| Return — change of mind | 126 | ₹5,04,388 |
| Return — faulty | 9 | ₹52,143 |
| Return — wrong item received | 1 | ₹2,899 |
| Warranty — repair/replacement not possible | 4 | ₹51,900 |
