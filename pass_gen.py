#!/usr/bin/env python3

import itertools
import argparse
import sys

#กำหนด dict ที่ใช้การดัดเเปลงตัวอักษร
TRANSFROM_RULES = {
    'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 
    's': ['5', '$'], 't': ['7'], 'l': ['1']
}

# ฟังก์ชันแปลงร่างคำ 
def transfrom_word(word: str) -> set[str]:
    
    
    # 1. รูปแบบพื้นฐาน: เก็บคำปกติ, ตัวแรกใหญ่, และตัวใหญ่ทั้งหมด
    mutations = {word, word.capitalize(), word.upper()} 
    
    options = []
    # วนดูทีละตัวอักษรของคำที่ถูกแปลงเป็นตัวเล็ก
    for char in word.lower():
        # ถ้ามีกฎการแทนที่: ให้เก็บตัวอักษรเดิม + ทางเลือกที่กลายพันธุ์
        if char in TRANSFROM_RULES:
            options.append([char] + TRANSFROM_RULES[char]) 
        # ถ้าไม่มีกฎ: ให้เก็บแค่ตัวอักษรเดิมเท่านั้น
        else:
            options.append([char])
            
    # 2. พลังผสมร่าง: ใช้ itertools.product สร้างการรวมชุดของทุกทางเลือก
    for combo in itertools.product(*options):
        mutations.add("".join(combo))

    return mutations # คืนค่าเป็น Set (กลุ่มคำที่ไม่ซ้ำกัน) ที่แปลงร่างแล้ว


#  main func ในการสร้าง Wordlist 

def gen_wordlist(keywords: list[str], years: list[str], SpecialSymbols: str, max_length: int = 17, limit: int = 0):
    
    final_passwords: set[str] = set() #กำหนดตัวเเปรเป็น set กันซ้ำ
    
    # สร้างชุดคำหลักที่ถูกแปลงร่างแล้ว
    mutated_keywords: set[str] = set()
    for keyword in keywords:
        mutated_keywords.update(transfrom_word(keyword))
        
    
    two_num = [f"{i:02d}" for i in range(100)] 
    symbol_list = list(SpecialSymbols)
    year_and_num = years + two_num  #เสริมตัวเลข 0-99 กรณีรหัสผ่านผู้ใช้ ใช้เลข 2 ตัวท้ายของปีเพื่อเพิ่มความหลากหลาย

    
   
    for p in itertools.product(mutated_keywords, year_and_num): #เอาค่าจาก mutated_keywords กับ year_and_num มาผสมกัน
        final_passwords.add("".join(p))
   
   
    for p in itertools.product(mutated_keywords, symbol_list, year_and_num): #เอาค่าจาก mutated_keywords กับ symbol_list และ year_and_num มาผสมกัน
        final_passwords.add("".join(p))
    
   
    for p in itertools.product(year_and_num, mutated_keywords): #เอาค่า year_and_num ขึ้นก่อนเพิ่มความหลากหลาย
        final_passwords.add("".join(p))
    
    
    for p in itertools.product(mutated_keywords, mutated_keywords): #ผสมคำหลักที่ถูกดัดเเปลงเเล้ว 2 คำ
        if p[0] != p[1]:
            final_passwords.add("".join(p))

   
   
    # 4. กรอง, จัดเรียง, พิมพ์ผลลัพธ์, และจำกัดจำนวน
    count = 0
    # ใช้ sorted() เพื่อให้รหัสผ่านเรียงตามตัวอักษร/ตัวเลข
    for password in sorted(list(final_passwords)):
        
        # *** NEW: เงื่อนไขการจำกัดคำ ***
        if limit > 0 and count >= limit:
            sys.stderr.write(f"[+] สร้าง Wordlist Susccess!😎😎😎 (limit: {limit} )\n")
            break # หยุด Loop ทันที
        # *** END NEW ***
            
        #เช็คความยาวรหัสผ่านก่อนส่งผลลัพธ์ไปเป็น txt 
        if len(password) <= max_length:
            sys.stdout.write(password + "\n") 
            count += 1
            
    # กรณีไม่มีการจำกัดจำนวนคำ จะเเสดงผลลัพธ์เมื่อจบการสร้างคำทั้งหมด
    if limit == 0 or count < limit:
        sys.stderr.write(f"Create wordlist Success!😎😎😎 : {count} \n")


#  ส่วนควบคุม (CLI - Argument Parser)
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        prog='./pass_gen.py',
        description="ยินดีต้อนรับสู่โปรแกรมสร้าง Wordlist ครับผมมมมม😘.",
        epilog="Example การใช้ :      ./pass_gen.py -k 'target' -y '2025' -n 100 > list.txt"
    )
    
   
   #กำหนด options ต่างๆ required=True คือจำเป็นต้องใส่
   
    parser.add_argument('-k', '--keywords', required=True, 
                        help='Comma-separated list of keywords.') 
   
    parser.add_argument('-y', '--years', required=True, 
                        help='Comma-separated list of years/digits.')
  
    parser.add_argument('-s', '--special-symbols', default='!@#$', 
                        help='String of special characters.')
    
    parser.add_argument('-l', '--max-lenght', type=int, default=15, 
                        help='Maximum length for passwords.')
    
    parser.add_argument('-n', '--limit', type=int, default=0, 
                        help='Maximum number of passwords to generate (0 for no limit).')
    
    args = parser.parse_args()
    
    # แปลง Input String ให้เป็น List เพื่อส่งเข้าฟังก์ชัน
    keywords_list = [k.strip() for k in args.keywords.split(',')]
    years_list = [y.strip() for y in args.years.split(',')]
    
    #เริ่มการสร้าง Wordlist 
    gen_wordlist(keywords_list, years_list, args.special_symbols, args.max_lenght, args.limit)
