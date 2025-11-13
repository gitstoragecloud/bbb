"""
範例 0：原始 Hadamard 測量範例
這是基於您提供的原始代碼
"""

# pip install qiskit[all]

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler


def main():
    """原始範例：Hadamard 閘和測量"""

    print("=== 原始範例：Hadamard 閘和測量 ===\n")

    # 建立一個只有 1 個 qubit 和 1 個經典位元（用來儲存測量結果）
    qc = QuantumCircuit(1, 1)

    # 對 qubit 套用 Hadamard Gate，讓它進入疊加態
    qc.h(0)

    # 測量 qubit，結果存到第 0 個經典位元
    qc.measure(0, 0)

    # 顯示電路圖
    print("量子電路圖:")
    print(qc.draw())
    print("\n")

    # 用模擬器執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()

    # 顯示測量結果
    counts = result.quasi_dists[0].binary_probabilities()

    print("測量結果 (1000 次):")
    print(counts)
    print("\n")

    # 分析結果
    prob_0 = counts.get('0', 0)
    prob_1 = counts.get('1', 0)

    print("結果分析:")
    print(f"  測量到 '0' 的機率: {prob_0:.1%}")
    print(f"  測量到 '1' 的機率: {prob_1:.1%}")
    print("\n")

    print("說明:")
    print("  Hadamard 閘將 |0⟩ 轉換為 (|0⟩ + |1⟩)/√2")
    print("  這是一個均等疊加態，測量時有 50% 機率得到 0 或 1")
    print("\n")

    # 儲存結果到文件
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("Hadamard 測量結果\n")
        f.write("=" * 50 + "\n")
        f.write(str(counts))
        f.write("\n\n")
        f.write(f"測量到 '0' 的機率: {prob_0:.1%}\n")
        f.write(f"測量到 '1' 的機率: {prob_1:.1%}\n")

    print("✓ 結果已儲存到 results.txt")


if __name__ == "__main__":
    main()
