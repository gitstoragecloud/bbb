"""
範例 5：實際應用
展示量子電路的實際應用場景
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import math


def quantum_coin_flip():
    """量子拋硬幣（公平隨機）"""
    print("=== 量子拋硬幣 ===")

    def flip_coin():
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        return "正面" if '0' in counts else "反面"

    print("拋 10 次量子硬幣:")
    results = [flip_coin() for _ in range(10)]
    print(f"  {results}")
    print(f"  正面: {results.count('正面')} 次")
    print(f"  反面: {results.count('反面')} 次")
    print("\n")


def quantum_dice():
    """量子骰子（1-6）"""
    print("=== 量子骰子 ===")

    def roll_dice():
        # 使用 3 個 qubits 可以產生 0-7 的數字
        # 我們取 1-6，如果得到 0 或 7 就重新擲
        while True:
            qc = QuantumCircuit(3, 3)

            # 所有 qubits 進入疊加態
            for i in range(3):
                qc.h(i)

            qc.measure([0, 1, 2], [0, 1, 2])

            sampler = Sampler()
            job = sampler.run(qc, shots=1)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()

            # 轉換為十進制
            binary = list(counts.keys())[0]
            number = int(binary, 2)

            # 如果在 1-6 範圍內，返回
            if 1 <= number <= 6:
                return number

    print("擲 10 次量子骰子:")
    results = [roll_dice() for _ in range(10)]
    print(f"  {results}")
    print(f"  統計: {dict((i, results.count(i)) for i in range(1, 7))}")
    print("\n")


def quantum_lottery():
    """量子樂透號碼生成器"""
    print("=== 量子樂透號碼生成器 ===")

    def generate_lottery_number(max_num=49, count=6):
        """生成不重複的樂透號碼"""
        numbers = set()

        while len(numbers) < count:
            # 需要的 bits
            n_bits = max_num.bit_length()

            qc = QuantumCircuit(n_bits, n_bits)

            for i in range(n_bits):
                qc.h(i)

            qc.measure(range(n_bits), range(n_bits))

            sampler = Sampler()
            job = sampler.run(qc, shots=1)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()

            binary = list(counts.keys())[0]
            number = int(binary, 2)

            # 確保在範圍內且不重複
            if 1 <= number <= max_num:
                numbers.add(number)

        return sorted(list(numbers))

    print("生成 3 組樂透號碼 (1-49, 選 6 個):")
    for i in range(3):
        lottery = generate_lottery_number()
        print(f"  第 {i+1} 組: {lottery}")

    print("\n")


def quantum_password_generator():
    """量子密碼生成器"""
    print("=== 量子密碼生成器 ===")

    def generate_password(length=12):
        """生成隨機密碼"""
        import string

        # 可用字符
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        n_chars = len(chars)

        password = ""

        for _ in range(length):
            # 需要的 bits
            n_bits = n_chars.bit_length()

            while True:
                qc = QuantumCircuit(n_bits, n_bits)

                for i in range(n_bits):
                    qc.h(i)

                qc.measure(range(n_bits), range(n_bits))

                sampler = Sampler()
                job = sampler.run(qc, shots=1)
                result = job.result()
                counts = result.quasi_dists[0].binary_probabilities()

                binary = list(counts.keys())[0]
                index = int(binary, 2)

                if index < n_chars:
                    password += chars[index]
                    break

        return password

    print("生成 3 個量子密碼 (長度 12):")
    for i in range(3):
        pwd = generate_password(12)
        print(f"  密碼 {i+1}: {pwd}")

    print("\n")


def quantum_shuffling():
    """量子洗牌"""
    print("=== 量子洗牌（撲克牌）===")

    def quantum_shuffle(items):
        """使用量子隨機性洗牌"""
        import random

        # 生成量子隨機種子
        n_bits = 32
        qc = QuantumCircuit(n_bits, n_bits)

        for i in range(n_bits):
            qc.h(i)

        qc.measure(range(n_bits), range(n_bits))

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        binary = list(counts.keys())[0]
        seed = int(binary, 2)

        # 使用量子種子初始化隨機數生成器
        random.seed(seed)
        shuffled = items.copy()
        random.shuffle(shuffled)

        return shuffled

    cards = ['A♠', 'K♠', 'Q♠', 'J♠', '10♠', '9♠', '8♠', '7♠']
    print(f"原始順序: {cards}")

    shuffled = quantum_shuffle(cards)
    print(f"洗牌後:   {shuffled}")
    print("\n")


def quantum_monte_carlo():
    """量子蒙地卡羅模擬（估計 π）"""
    print("=== 量子蒙地卡羅（估計 π）===")

    def estimate_pi(n_samples=1000):
        """使用量子隨機數估計 π"""
        # 生成 n_samples 個隨機點 (x, y)
        # 計算落在單位圓內的點數

        inside_circle = 0

        for _ in range(n_samples):
            # 生成隨機 x 座標 (0-1)
            qc_x = QuantumCircuit(10, 10)  # 10 bits 精度
            for i in range(10):
                qc_x.h(i)
            qc_x.measure(range(10), range(10))

            sampler = Sampler()
            job = sampler.run(qc_x, shots=1)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()
            x = int(list(counts.keys())[0], 2) / (2**10)

            # 生成隨機 y 座標 (0-1)
            qc_y = QuantumCircuit(10, 10)
            for i in range(10):
                qc_y.h(i)
            qc_y.measure(range(10), range(10))

            job = sampler.run(qc_y, shots=1)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()
            y = int(list(counts.keys())[0], 2) / (2**10)

            # 檢查是否在圓內
            if x*x + y*y <= 1:
                inside_circle += 1

        # π ≈ 4 * (inside_circle / n_samples)
        pi_estimate = 4 * inside_circle / n_samples
        return pi_estimate

    print("使用量子隨機數估計 π (100 個樣本):")
    pi_est = estimate_pi(100)
    print(f"  估計值: {pi_est:.4f}")
    print(f"  真實值: {math.pi:.4f}")
    print(f"  誤差:   {abs(pi_est - math.pi):.4f}")
    print("\n")


def quantum_game_rng():
    """量子遊戲隨機數生成器"""
    print("=== 量子遊戲 RNG ===")

    def critical_hit_check(crit_chance=0.15):
        """檢查是否暴擊（預設 15% 機率）"""
        # 使用旋轉閘創建特定機率
        angle = 2 * math.asin(math.sqrt(crit_chance))

        qc = QuantumCircuit(1, 1)
        qc.ry(angle, 0)
        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        return '1' in counts  # True = 暴擊

    def loot_drop(drop_rate=0.05):
        """檢查是否掉落寶物（預設 5% 機率）"""
        angle = 2 * math.asin(math.sqrt(drop_rate))

        qc = QuantumCircuit(1, 1)
        qc.ry(angle, 0)
        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        return '1' in counts  # True = 掉落

    # 模擬 100 次攻擊
    print("模擬 100 次攻擊（15% 暴擊率）:")
    crits = sum(critical_hit_check(0.15) for _ in range(100))
    print(f"  暴擊次數: {crits}/100 ({crits}%)")

    # 模擬 100 次打怪
    print("\n模擬 100 次打怪（5% 寶物掉落率）:")
    drops = sum(loot_drop(0.05) for _ in range(100))
    print(f"  掉落次數: {drops}/100 ({drops}%)")

    print("\n")


def quantum_decision_maker():
    """量子決策器"""
    print("=== 量子決策器 ===")

    def make_decision(options):
        """從多個選項中隨機選擇一個"""
        n = len(options)
        n_bits = n.bit_length()

        while True:
            qc = QuantumCircuit(n_bits, n_bits)

            for i in range(n_bits):
                qc.h(i)

            qc.measure(range(n_bits), range(n_bits))

            sampler = Sampler()
            job = sampler.run(qc, shots=1)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()

            binary = list(counts.keys())[0]
            index = int(binary, 2)

            if index < n:
                return options[index]

    # 範例：選擇午餐
    lunch_options = ["披薩", "壽司", "漢堡", "沙拉", "麵食"]
    print(f"午餐選項: {lunch_options}")
    choice = make_decision(lunch_options)
    print(f"量子決策: {choice}")

    # 範例：選擇電影
    movies = ["科幻片", "動作片", "喜劇片", "驚悚片"]
    print(f"\n電影選項: {movies}")
    choice = make_decision(movies)
    print(f"量子決策: {choice}")

    print("\n")


def quantum_weighted_choice():
    """量子加權選擇"""
    print("=== 量子加權選擇 ===")

    def weighted_choice():
        """使用量子態創建加權選擇"""
        # 例如：選項 A (70%), 選項 B (30%)
        qc = QuantumCircuit(1, 1)

        # 旋轉到特定角度以獲得 70/30 分布
        angle = 2 * math.asin(math.sqrt(0.3))
        qc.ry(angle, 0)

        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        return "選項 A (70%)" if '0' in counts else "選項 B (30%)"

    # 測試 100 次
    print("測試加權選擇 100 次:")
    results = [weighted_choice() for _ in range(100)]
    count_a = results.count("選項 A (70%)")
    count_b = results.count("選項 B (30%)")

    print(f"  選項 A: {count_a} 次")
    print(f"  選項 B: {count_b} 次")
    print("\n")


def save_all_results():
    """執行所有範例"""
    print("執行所有實際應用範例...\n")

    quantum_coin_flip()
    quantum_dice()
    quantum_lottery()
    quantum_password_generator()
    quantum_shuffling()
    quantum_monte_carlo()
    quantum_game_rng()
    quantum_decision_maker()
    quantum_weighted_choice()

    with open("example_05_results.txt", "w", encoding="utf-8") as f:
        f.write("量子電路實際應用範例已執行\n")
        f.write("=" * 50 + "\n")
        f.write("請查看控制台輸出以查看詳細結果\n")


if __name__ == "__main__":
    print("量子電路範例 5：實際應用\n")
    print("=" * 60)

    save_all_results()

    print("✓ 所有範例執行完畢！結果已儲存到 example_05_results.txt")
