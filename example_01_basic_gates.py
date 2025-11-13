"""
範例 1：基本量子閘操作
展示 X, Y, Z 閘的效果
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler


def pauli_x_gate():
    """Pauli-X 閘（量子 NOT 閘）"""
    print("=== Pauli-X 閘（翻轉 qubit）===")

    # 創建電路
    qc = QuantumCircuit(1, 1)

    # 應用 X 閘（|0⟩ → |1⟩）
    qc.x(0)

    # 測量
    qc.measure(0, 0)

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% 得到 '1'（因為 X 閘把 |0⟩ 翻轉成 |1⟩）")
    print(qc.draw())
    print("\n")

    return counts


def pauli_z_gate():
    """Pauli-Z 閘（相位翻轉）"""
    print("=== Pauli-Z 閘（相位翻轉）===")

    # 創建電路
    qc = QuantumCircuit(1, 1)

    # 先創建疊加態
    qc.h(0)

    # 應用 Z 閘
    qc.z(0)

    # 再應用 Hadamard 回到基態
    qc.h(0)

    # 測量
    qc.measure(0, 0)

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% 得到 '1'（Z 閘改變相位，干涉後得到 |1⟩）")
    print(qc.draw())
    print("\n")

    return counts


def rotation_gates():
    """旋轉閘（RY 閘）"""
    print("=== 旋轉閘（RY π/4）===")

    import math

    # 創建電路
    qc = QuantumCircuit(1, 1)

    # 應用 RY 閘（繞 Y 軸旋轉 π/4）
    qc.ry(math.pi/4, 0)

    # 測量
    qc.measure(0, 0)

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 85% '0' 和 15% '1'")
    print(qc.draw())
    print("\n")

    return counts


def multiple_hadamard():
    """多次 Hadamard（干涉效應）"""
    print("=== 兩次 Hadamard（互相抵消）===")

    # 創建電路
    qc = QuantumCircuit(1, 1)

    # 第一次 Hadamard：|0⟩ → (|0⟩ + |1⟩)/√2
    qc.h(0)

    # 第二次 Hadamard：回到 |0⟩
    qc.h(0)

    # 測量
    qc.measure(0, 0)

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% 得到 '0'（兩次 Hadamard 互相抵消）")
    print(qc.draw())
    print("\n")

    return counts


def x_then_hadamard():
    """先翻轉再疊加"""
    print("=== 先 X 閘再 Hadamard ===")

    # 創建電路
    qc = QuantumCircuit(1, 1)

    # X 閘：|0⟩ → |1⟩
    qc.x(0)

    # Hadamard：|1⟩ → (|0⟩ - |1⟩)/√2
    qc.h(0)

    # 測量
    qc.measure(0, 0)

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '0' 和 50% '1'（疊加態）")
    print(qc.draw())
    print("\n")

    # 儲存結果
    with open("example_01_results.txt", "w", encoding="utf-8") as f:
        f.write("基本量子閘操作結果\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"X 閘後: {counts}\n")

    return counts


if __name__ == "__main__":
    print("量子電路範例 1：基本量子閘操作\n")
    print("=" * 60)

    pauli_x_gate()
    pauli_z_gate()
    rotation_gates()
    multiple_hadamard()
    x_then_hadamard()

    print("✓ 所有範例執行完畢！結果已儲存到 example_01_results.txt")
