"""
範例 3：量子疊加與干涉
展示量子疊加態和干涉效應
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import math


def equal_superposition():
    """均等疊加態"""
    print("=== 均等疊加態（50-50）===")

    qc = QuantumCircuit(1, 1)

    # Hadamard 創建均等疊加
    qc.h(0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '0' 和 50% '1'")
    print(qc.draw())
    print("\n")

    return counts


def unequal_superposition():
    """不均等疊加態（使用旋轉閘）"""
    print("=== 不均等疊加態（70-30）===")

    qc = QuantumCircuit(1, 1)

    # 使用 RY 閘創建不均等疊加
    # 角度 ≈ 1.287 弧度 會給出約 70% |0⟩ 和 30% |1⟩
    qc.ry(1.287, 0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 70% '0' 和 30% '1'")
    print(qc.draw())
    print("\n")

    return counts


def constructive_interference():
    """建設性干涉"""
    print("=== 建設性干涉（兩次 Hadamard）===")

    qc = QuantumCircuit(1, 1)

    # 兩次 Hadamard：干涉讓我們回到 |0⟩
    qc.h(0)
    qc.h(0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% '0'（完全建設性干涉）")
    print("說明: 兩次 Hadamard 互相抵消")
    print(qc.draw())
    print("\n")

    return counts


def destructive_interference():
    """破壞性干涉"""
    print("=== 破壞性干涉（X-H-H）===")

    qc = QuantumCircuit(1, 1)

    # X 閘 + 兩次 Hadamard
    qc.x(0)
    qc.h(0)
    qc.h(0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% '1'")
    print(qc.draw())
    print("\n")

    return counts


def phase_kickback():
    """相位反沖（Phase Kickback）"""
    print("=== 相位反沖 ===")

    qc = QuantumCircuit(1, 1)

    # 創建疊加態
    qc.h(0)

    # 應用 Z 閘（改變相位）
    qc.z(0)

    # 再次 Hadamard（觀察相位變化）
    qc.h(0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 100% '1'（Z 閘改變相位導致干涉）")
    print(qc.draw())
    print("\n")

    return counts


def multi_qubit_superposition():
    """多 Qubit 疊加態"""
    print("=== 多 Qubit 疊加態（3 qubits）===")

    qc = QuantumCircuit(3, 3)

    # 所有 qubits 進入疊加態
    qc.h(0)
    qc.h(1)
    qc.h(2)

    qc.measure([0, 1, 2], [0, 1, 2])

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 8 種狀態均等分布（每種約 12.5%）")
    print(f"可能狀態數: 2^3 = 8")
    print(qc.draw())
    print("\n")

    return counts


def mach_zehnder_interferometer():
    """Mach-Zehnder 干涉儀（量子版本）"""
    print("=== Mach-Zehnder 干涉儀 ===")

    qc = QuantumCircuit(1, 1)

    # 第一個分束器（Hadamard）
    qc.h(0)

    # 相位偏移（可調整）
    phase = math.pi  # 改變這個值會改變干涉結果
    qc.p(phase, 0)

    # 第二個分束器（Hadamard）
    qc.h(0)

    qc.measure(0, 0)

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果 (相位 = π): {counts}")
    print("預期: 100% '1'（相位 π 導致完全破壞性干涉）")
    print(qc.draw())
    print("\n")

    # 測試不同相位
    print("測試不同相位:")
    for p in [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]:
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.p(p, 0)
        qc.h(0)
        qc.measure(0, 0)

        sampler = Sampler()
        job = sampler.run(qc, shots=1000)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()

        prob_0 = counts.get('0', 0)
        print(f"  相位 {p:.2f}: P(0) = {prob_0:.3f}")

    print("\n")

    return counts


def quantum_walk():
    """簡單的量子隨機行走"""
    print("=== 量子隨機行走（簡化版）===")

    qc = QuantumCircuit(2, 2)

    # 初始化：位置 qubit 在 |0⟩，方向 qubit 在疊加態
    qc.h(0)  # 方向 qubit

    # 步驟 1
    qc.cx(0, 1)  # 根據方向移動

    # 步驟 2：改變方向
    qc.h(0)

    # 步驟 3
    qc.cx(0, 1)

    qc.measure([0, 1], [0, 1])

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("說明: 量子行走展示了干涉效應")
    print(qc.draw())
    print("\n")

    return counts


def save_all_results():
    """執行所有範例並儲存結果"""
    results = {}

    results['equal_super'] = equal_superposition()
    results['unequal_super'] = unequal_superposition()
    results['constructive'] = constructive_interference()
    results['destructive'] = destructive_interference()
    results['phase_kickback'] = phase_kickback()
    results['multi_super'] = multi_qubit_superposition()
    results['interferometer'] = mach_zehnder_interferometer()
    results['quantum_walk'] = quantum_walk()

    # 儲存到檔案
    with open("example_03_results.txt", "w", encoding="utf-8") as f:
        f.write("量子疊加與干涉範例結果\n")
        f.write("=" * 50 + "\n\n")

        for key, value in results.items():
            f.write(f"{key}:\n{value}\n\n")

    return results


if __name__ == "__main__":
    print("量子電路範例 3：量子疊加與干涉\n")
    print("=" * 60)

    save_all_results()

    print("✓ 所有範例執行完畢！結果已儲存到 example_03_results.txt")
