from abc import ABC, abstractmethod
from tabulate import tabulate

class Champion:
    def __init__(self,champion_id : str, name : str, base_hp :int, base_atk :int):
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk
        
    @abstractmethod
    def calculate_skill_damage(self):
        pass
    
    def get_combat_power(self):
        return self.base_hp + self.calculate_skill_damage() * 1.5
    
    def __add__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        elif isinstance(other, (int, float)):
            return self.get_combat_power() + other
        
    def __gt__(self, other):
        return self.get_combat_power() > other.get_combat_power()
    
    
class Warrior(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, shield_bonus ):
        self.shield_bonus  = shield_bonus 
        super().__init__(champion_id, name, base_hp, base_atk)
        
    def calculate_skill_damage(self):
        return self.base_atk * 2 + self.shield_bonus
    
class Mage(Champion):
    def __init__(self, champion_id, name, base_hp, base_atk, ability_power ):
        self.ability_power  = ability_power 
        super().__init__(champion_id, name, base_hp, base_atk)
    
    def calculate_skill_damage(self):
        return self.base_atk * 2 + self.ability_power
    
'''
*** Chức năng 1: Hiển thị bể tướng hiện có
Ban đầu hệ thống tự động khởi tạo sẵn một danh sách champion_pool gồm ít nhất 3 tướng (Ví dụ: 2 Warrior, 1 Mage).

In ra màn hình danh sách rõ ràng, phân biệt rõ Tướng đó thuộc hệ nào, các chỉ số riêng ra sao.
'''
def display(champ_list):
    table = []
    for champ in champ_list:
        power = champ.get_combat_power()
        champ_class = champ.__class__.__name__
        if isinstance(champ, Warrior):
            unique_stat = f"Armor: {champ.shield_bonus}"
        elif isinstance(champ, Mage):
            unique_stat = f"Mana: {champ.ability_power}"
        list = [champ.champion_id, champ.name, champ_class, champ.base_hp, champ.base_atk, unique_stat, power ]
        table.append(list)
    print("--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    print(tabulate(table, headers=['Mã', "Tên tướng", 'Hệ', 'HP', 'ATK', 'Chỉ số riêng', 'Chiến lực'], tablefmt='github'))
    
'''
*** Chức năng 2: Thêm quân cờ mới
Cho phép người dùng nhập thông tin để tạo tướng mới.

Người dùng chọn Hệ (1 - Warrior, 2 - Mage), sau đó nhập các thông tin chung và thuộc tính riêng tương ứng.
'''
def find_index(id, champ_list):
    for index, champ in enumerate(champ_list):
        if id == champ.champion_id:
            return index
    return -1

def add_champ(champ_list):
    print("--- TẠO TƯỚNG ---")
    id_inp = input("Nhập mã tướng: ").strip().upper()
    if find_index(id_inp, champ_list) != -1:
        print("Mã tướng đã tồn tại")
        return
    new_name = input("Nhập tên tướng: ").strip().title()
    choice = input("Chọn Hệ (1 - Warrior, 2 - Mage) ").strip()
    if choice == '1':
        class_champ = Warrior
        unique = "Armor"
    elif choice == '2':
        class_champ = Mage
        unique = "Mana"
    else:
        print("Lỗi cú pháp")
        return
    hp = int(input("Nhập HP: ").strip())
    atk = int(input("Nhập ATK: ").strip())
    unique_stat = int(input(f"Nhập {unique}: ").strip())
    new_champ = class_champ(id_inp, new_name, hp, atk, unique_stat)
    champ_list.append(new_champ)
    print("Thêm tướng thành công!")
    print(f"Mã: {new_champ.champion_id} | Tên: {new_champ.name} | Chiến lực: {new_champ.get_combat_power()}")
    
'''
*** Chức năng 3: So sánh 2 quân cờ
Yêu cầu người dùng nhập vào 2 Mã quân cờ cần so sánh.

Hệ thống tìm kiếm trong bể tướng, sau đó dùng toán tử > (ví dụ: if champion1 > champion2:) để phân định và in ra kết quả tướng nào mạnh hơn. ( gợi ý: sử dụng nạp chồng toán tử )
'''
def compare_champ(champ_list):
    print("--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    id_1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    id_2 = input("Nhập mã tướng thứ hai: ").strip().upper()
    index_1 = find_index(id_1, champ_list)
    index_2 = find_index(id_2, champ_list)
    
    if index_1 == -1 or index_2 == -1:
        print("Mã tướng không tồn tại!!!")
        return
    champ_1 = champ_list[index_1]
    champ_2 = champ_list[index_2]
    print("Thông tin so sánh:")
    print(f"{champ_1.champion_id} - {champ_1.name} | Hệ: {champ_1.__class__.__name__} | Chiến lực: {champ_1.get_combat_power()}")
    print(f"{champ_2.champion_id} - {champ_2.name} | Hệ: {champ_2.__class__.__name__} | Chiến lực: {champ_2.get_combat_power()}")
    
    if champ_1.get_combat_power() > champ_2.get_combat_power():
        winner = f"{champ_1.champion_id} - {champ_1.name}"
        loser = f"{champ_2.champion_id} - {champ_2.name}"
    else:
        winner = f"{champ_2.champion_id} - {champ_2.name}"
        loser = f"{champ_1.champion_id} - {champ_1.name}"
        
    print(f"Kết quả:{winner} mạnh hơn {loser}.")
    
'''
*** Chức năng 4: Tính tổng chiến lực Đội Hình Ra Sân
Người dùng nhập vào danh sách các mã quân cờ muốn đưa vào đội hình (phân tách bằng dấu phẩy, ví dụ: WAR01, MAG01).

Hệ thống duyệt qua danh sách, sử dụng toán tử + để cộng dồn điểm chiến lực của các tướng này lại và in ra tổng điểm sức mạnh của toàn đội hình.  ( gợi ý: sử dụng nạp chồng toán tử )
'''
def caculate_power(champ_list):
    total_power = 0
    id_str = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ").strip().upper()
    list_id = id_str.split(",")
    print('Danh sách đội hình:')
    for i, id in enumerate(list_id,start=1):
        list_id[i-1] = id.strip()
        for champ in champ_list:
            if champ.champion_id == list_id[i-1]:
                print(f"{i}. {champ.champion_id} - {champ.name} | Chiến lực: {champ.get_combat_power()}")
                total_power += champ.get_combat_power()
                break
            
    print(f'Tổng chiến lực đội hình: {total_power} ')

    
    
    
    
def main():
    champion_pool = [
    Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
    Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
    Mage("MAG01", "Rikkei Wizard", 800, 500, 250)
]
    while True:
        choice = input("""
============MENU============
1: Hiển thị bể tướng hiện có
2: Thêm quân cờ mới                       
3: So sánh 2 quân cờ
4: Tính tổng chiến lực Đội Hình Ra Sân
5: Thoát chương trình   
=============================  
Mời bạn nhập lựa chọn: """).strip()
        print()
        if choice.isdigit():
            choice = int(choice)
        else:
            print("Vui lòng nhập số nguyên")
            continue
        
        match choice:
            case 1:
                display(champion_pool)
                
            case 2:
                add_champ(champion_pool)
                
            case 3:
                compare_champ(champion_pool)
                
            case 4:
                caculate_power(champion_pool)
                
            case 5:
                print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
                break
            
            case _:
                print("lỗi cú pháp!!!!")
                
if __name__ == "__main__":
    main()                