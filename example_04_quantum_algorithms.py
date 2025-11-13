"""
範例 4：量子演算法
展示經典的量子演算法：Deutsch、Bernstein-Vazirani、量子隨機數生成
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import math


def quantum_random_number_generator():
    """量子隨機數生成器"""
    print("=== 量子隨機數生成器 ===")

    def generate_random_bit():
        """生成單個隨機位元"""
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        # 返回測量結果
        return '1' if counts.get('1', 0) > 0.5 else '0'

    def generate_random_byte():
        """生成 8 位元隨機數"""
        qc = QuantumCircuit(8, 8)

        # 所有 qubits 進入疊加態
        for i in range(8):
            qc.h(i)

        # 測量所有
        qc.measure(range(8), range(8))

        sampler = Sampler()
        job = sampler.run(qc, shots=1)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        # 取得結果（二進制字串）
        binary = list(counts.keys())[0]
        decimal = int(binary, 2)

        return binary, decimal

    print("生成 10 個隨機位元:")
    bits = [generate_random_bit() for _ in range(10)]
    print(f"  {''.join(bits)}")

    print("\n生成 5 個隨機字節 (0-255):")
    for i in range(5):
        binary, decimal = generate_random_byte()
        print(f"  {i+1}. 二進制: {binary} → 十進制: {decimal}")

    print(qc.draw())
    print("\n")


def deutsch_algorithm():
    """Deutsch 演算法（判斷函數是常數還是平衡）"""
    print("=== Deutsch 演算法 ===")

    def deutsch_circuit(oracle_type='balanced'):
        """
        oracle_type: 'constant_0', 'constant_1', 'balanced_identity', 'balanced_negation'
        """
        qc = QuantumCircuit(2, 1)

        # 初始化
        qc.x(1)  # 輔助 qubit 設為 |1⟩
        qc.h(0)  # 輸入 qubit 進入疊加態
        qc.h(1)  # 輔助 qubit 進入 |-⟩ 態

        # Oracle（根據類型）
        qc.barrier()
        if oracle_type == 'constant_0':
            # 什麼都不做
            pass
        elif oracle_type == 'constant_1':
            # 翻轉輔助 qubit
            qc.x(1)
        elif oracle_type == 'balanced_identity':
            # CNOT: 如果輸入是 1，翻轉輔助
            qc.cx(0, 1)
        elif oracle_type == 'balanced_negation':
            # 先翻轉輸入，再 CNOT
            qc.x(0)
            qc.cx(0, 1)
            qc.x(0)

        qc.barrier()

        # 最後的 Hadamard
        qc.h(0)

        # 只測量第一個 qubit
        qc.measure(0, 0)

        return qc

    # 測試不同的 oracle
    oracle_types = ['constant_0', 'constant_1', 'balanced_identity', 'balanced_negation']

    for oracle in oracle_types:
        qc = deutsch_circuit(oracle)

        sampler = Sampler()
        job = sampler.run(qc, shots=1000)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        result_bit = '0' if counts.get('0', 0) > 0.5 else '1'
        function_type = '常數' if result_bit == '0' else '平衡'

        print(f"Oracle: {oracle:20} → 測量結果: {result_bit} → 函數類型: {function_type}")

    print("\n電路圖 (balanced_identity):")
    print(deutsch_circuit('balanced_identity').draw())
    print("\n")


def bernstein_vazirani_algorithm():
    """Bernstein-Vazirani 演算法（找出隱藏的位元串）"""
    print("=== Bernstein-Vazirani 演算法 ===")

    # 隱藏的位元串（例如 '101'）
    hidden_string = '101'
    n = len(hidden_string)

    print(f"隱藏的位元串: {hidden_string}")

    # 創建電路
    qc = QuantumCircuit(n + 1, n)

    # 初始化
    qc.x(n)  # 輔助 qubit 設為 |1⟩

    # 所有 qubits 進入疊加態
    for i in range(n + 1):
        qc.h(i)

    # Oracle: 根據隱藏位元串
    qc.barrier()
    for i, bit in enumerate(reversed(hidden_string)):
        if bit == '1':
            qc.cx(i, n)
    qc.barrier()

    # 最後的 Hadamard（不包括輔助 qubit）
    for i in range(n):
        qc.h(i)

    # 測量
    qc.measure(range(n), range(n))

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    measured_string = max(counts, key=counts.get)

    print(f"測量結果: {measured_string}")
    print(f"正確！" if measured_string == hidden_string else f"錯誤！")
    print(f"只需運行 1 次！（傳統演算法需要 {2**n} 次）")
    print(qc.draw())
    print("\n")


def deutsch_jozsa_algorithm():
    """Deutsch-Jozsa 演算法（多位元版本的 Deutsch）"""
    print("=== Deutsch-Jozsa 演算法 ===")

    n = 3  # 3 個輸入 qubits

    def dj_circuit(oracle_type='balanced'):
        """
        oracle_type: 'constant' 或 'balanced'
        """
        qc = QuantumCircuit(n + 1, n)

        # 初始化
        qc.x(n)

        # 所有 qubits 進入疊加態
        for i in range(n + 1):
            qc.h(i)

        # Oracle
        qc.barrier()
        if oracle_type == 'constant':
            # 常數函數：什麼都不做
            pass
        else:  # balanced
            # 平衡函數：CNOT 所有輸入到輔助
            for i in range(n):
                qc.cx(i, n)

        qc.barrier()

        # 最後的 Hadamard
        for i in range(n):
            qc.h(i)

        # 測量
        qc.measure(range(n), range(n))

        return qc

    # 測試常數函數
    print("測試常數函數:")
    qc_constant = dj_circuit('constant')
    sampler = Sampler()
    job = sampler.run(qc_constant, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    all_zeros = counts.get('0' * n, 0)
    print(f"  測量到 '{'0' * n}' 的機率: {all_zeros:.3f}")
    print(f"  結論: {'常數函數' if all_zeros > 0.9 else '平衡函數'}")

    # 測試平衡函數
    print("\n測試平衡函數:")
    qc_balanced = dj_circuit('balanced')
    job = sampler.run(qc_balanced, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    all_zeros = counts.get('0' * n, 0)
    print(f"  測量到 '{'0' * n}' 的機率: {all_zeros:.3f}")
    print(f"  結論: {'常數函數' if all_zeros > 0.9 else '平衡函數'}")

    print("\n電路圖 (balanced):")
    print(qc_balanced.draw())
    print("\n")


def quantum_teleportation():
    """量子隱形傳態（簡化版）"""
    print("=== 量子隱形傳態 ===")

    qc = QuantumCircuit(3, 3)

    # 準備要傳送的狀態（qubit 0）
    # 例如：|ψ⟩ = cos(π/4)|0⟩ + sin(π/4)|1⟩
    qc.ry(math.pi/4, 0)

    qc.barrier()

    # 創建糾纏對（qubits 1 和 2）
    qc.h(1)
    qc.cx(1, 2)

    qc.barrier()

    # Alice 的操作
    qc.cx(0, 1)
    qc.h(0)

    # Alice 測量
    qc.measure([0, 1], [0, 1])

    qc.barrier()

    # Bob 的修正操作（基於 Alice 的測量結果）
    qc.cx(1, 2)
    qc.cz(0, 2)

    # 最終測量 qubit 2（應該是傳送的狀態）
    qc.measure(2, 2)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("說明: qubit 0 的狀態被「傳送」到 qubit 2")
    print(qc.draw())
    print("\n")


def quantum_phase_estimation_simple():
    """量子相位估計（簡化版）"""
    print("=== 量子相位估計（簡化版）===")

    # 估計 T 閘的相位（應該是 π/4）
    qc = QuantumCircuit(2, 1)

    # 準備
    qc.h(0)  # 計數 qubit
    qc.x(1)  # 特徵態 |1⟩

    # 受控操作
    qc.cp(math.pi/4, 0, 1)  # Controlled-Phase

    # 反向 QFT（簡化版：只有 Hadamard）
    qc.h(0)

    # 測量
    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("說明: 用於估計量子閘的相位")
    print(qc.draw())
    print("\n")


def save_all_results():
    """執行所有範例"""
    print("執行所有量子演算法範例...\n")

    quantum_random_number_generator()
    deutsch_algorithm()
    bernstein_vazirani_algorithm()
    deutsch_jozsa_algorithm()
    quantum_teleportation()
    quantum_phase_estimation_simple()

    with open("example_04_results.txt", "w", encoding="utf-8") as f:
        f.write("量子演算法範例已執行\n")
        f.write("=" * 50 + "\n")
        f.write("請查看控制台輸出以查看詳細結果\n")


if __name__ == "__main__":
    print("量子電路範例 4：量子演算法\n")
    print("=" * 60)

    save_all_results()

    print("✓ 所有範例執行完畢！結果已儲存到 example_04_results.txt")
