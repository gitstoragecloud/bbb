"""
範例 2：量子糾纏（Entanglement）
展示貝爾態和 GHZ 態
"""

from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler


def bell_state():
    """貝爾態（最簡單的糾纏態）"""
    print("=== 貝爾態（Bell State）===")

    # 創建 2-qubit 電路
    qc = QuantumCircuit(2, 2)

    # 步驟 1：Hadamard 讓第一個 qubit 進入疊加態
    qc.h(0)

    # 步驟 2：CNOT 創建糾纏
    qc.cx(0, 1)

    # 測量兩個 qubits
    qc.measure([0, 1], [0, 1])

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '00' 和 50% '11'")
    print("注意: 不會出現 '01' 或 '10'，因為兩個 qubits 完全糾纏！")
    print(qc.draw())
    print("\n")

    return counts


def bell_state_phi_plus():
    """貝爾態 Φ+ = (|00⟩ + |11⟩)/√2"""
    print("=== 貝爾態 Φ+ ===")

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print(qc.draw())
    print("\n")

    return counts


def bell_state_psi_plus():
    """貝爾態 Ψ+ = (|01⟩ + |10⟩)/√2"""
    print("=== 貝爾態 Ψ+ ===")

    qc = QuantumCircuit(2, 2)

    # X 閘讓第二個 qubit 變成 |1⟩
    qc.x(1)

    # 創建糾纏
    qc.h(0)
    qc.cx(0, 1)

    qc.measure([0, 1], [0, 1])

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '01' 和 50% '10'")
    print(qc.draw())
    print("\n")

    return counts


def ghz_state_3qubits():
    """GHZ 態（3-qubit 糾纏）"""
    print("=== GHZ 態（3-qubit 糾纏）===")

    # 創建 3-qubit 電路
    qc = QuantumCircuit(3, 3)

    # 創建 GHZ 態
    qc.h(0)           # 第一個 qubit 進入疊加態
    qc.cx(0, 1)       # 糾纏第二個 qubit
    qc.cx(1, 2)       # 糾纏第三個 qubit

    # 測量所有 qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '000' 和 50% '111'")
    print("注意: 三個 qubits 完全糾纏，要麼全是 0，要麼全是 1！")
    print(qc.draw())
    print("\n")

    return counts


def ghz_state_4qubits():
    """GHZ 態（4-qubit 糾纏）"""
    print("=== GHZ 態（4-qubit 糾纏）===")

    # 創建 4-qubit 電路
    qc = QuantumCircuit(4, 4)

    # 創建 GHZ 態
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)

    # 測量所有 qubits
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

    # 執行
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 50% '0000' 和 50% '1111'")
    print(qc.draw())
    print("\n")

    return counts


def partial_entanglement():
    """部分糾纏（3 個 qubits，只有 2 個糾纏）"""
    print("=== 部分糾纏 ===")

    qc = QuantumCircuit(3, 3)

    # qubit 0 和 1 糾纏
    qc.h(0)
    qc.cx(0, 1)

    # qubit 2 保持獨立，進入疊加態
    qc.h(2)

    qc.measure([0, 1, 2], [0, 1, 2])

    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()

    print(f"結果: {counts}")
    print("預期: 約 25% 的機率得到 '000', '001', '110', '111'")
    print("說明: qubit 0 和 1 糾纏，qubit 2 獨立")
    print(qc.draw())
    print("\n")

    return counts


def save_all_results():
    """執行所有範例並儲存結果"""
    results = {}

    results['bell'] = bell_state()
    results['psi_plus'] = bell_state_psi_plus()
    results['ghz_3'] = ghz_state_3qubits()
    results['ghz_4'] = ghz_state_4qubits()
    results['partial'] = partial_entanglement()

    # 儲存到檔案
    with open("example_02_results.txt", "w", encoding="utf-8") as f:
        f.write("量子糾纏範例結果\n")
        f.write("=" * 50 + "\n\n")

        f.write("貝爾態 (Φ+):\n")
        f.write(f"{results['bell']}\n\n")

        f.write("貝爾態 (Ψ+):\n")
        f.write(f"{results['psi_plus']}\n\n")

        f.write("GHZ 態 (3-qubit):\n")
        f.write(f"{results['ghz_3']}\n\n")

        f.write("GHZ 態 (4-qubit):\n")
        f.write(f"{results['ghz_4']}\n\n")

        f.write("部分糾纏:\n")
        f.write(f"{results['partial']}\n")

    return results


if __name__ == "__main__":
    print("量子電路範例 2：量子糾纏\n")
    print("=" * 60)

    save_all_results()

    print("✓ 所有範例執行完畢！結果已儲存到 example_02_results.txt")
