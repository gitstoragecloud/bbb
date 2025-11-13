# Qiskit 量子電路範例集

這是一套完整的 Qiskit 量子電路範例程式，從基礎到進階，涵蓋量子計算的各個方面。

## 📚 範例列表

### 範例 1：基本量子閘操作 (`example_01_basic_gates.py`)

展示最基本的量子閘及其效果。

**涵蓋內容：**
- ✓ Pauli-X 閘（量子 NOT）
- ✓ Pauli-Z 閘（相位翻轉）
- ✓ Hadamard 閘（創建疊加態）
- ✓ 旋轉閘（RY）
- ✓ 多次 Hadamard（干涉效應）

**執行方式：**
```bash
python example_01_basic_gates.py
```

**學習重點：**
- 理解單量子位元閘的作用
- 觀察量子態的轉換
- 體驗量子干涉現象

---

### 範例 2：量子糾纏 (`example_02_entanglement.py`)

展示量子糾纏現象，包括貝爾態和 GHZ 態。

**涵蓋內容：**
- ✓ 貝爾態（2-qubit 糾纏）
- ✓ 四種貝爾態（Φ+, Φ-, Ψ+, Ψ-）
- ✓ GHZ 態（3-qubit 和 4-qubit 糾纏）
- ✓ 部分糾纏

**執行方式：**
```bash
python example_02_entanglement.py
```

**學習重點：**
- 理解量子糾纏的概念
- 觀察糾纏態的測量結果
- 區分完全糾纏和部分糾纏

**範例輸出：**
```
貝爾態結果: {'00': 0.501, '11': 0.499}
→ 兩個 qubits 完全關聯！
```

---

### 範例 3：量子疊加與干涉 (`example_03_superposition_interference.py`)

深入探討量子疊加態和干涉效應。

**涵蓋內容：**
- ✓ 均等疊加態（50-50）
- ✓ 不均等疊加態（自訂機率）
- ✓ 建設性干涉
- ✓ 破壞性干涉
- ✓ 相位反沖
- ✓ Mach-Zehnder 干涉儀
- ✓ 量子隨機行走

**執行方式：**
```bash
python example_03_superposition_interference.py
```

**學習重點：**
- 掌握疊加態的創建和控制
- 理解量子干涉原理
- 學習相位的重要性

---

### 範例 4：量子演算法 (`example_04_quantum_algorithms.py`)

實作經典的量子演算法。

**涵蓋內容：**
- ✓ 量子隨機數生成器
- ✓ Deutsch 演算法（判斷函數類型）
- ✓ Bernstein-Vazirani 演算法（找出隱藏字串）
- ✓ Deutsch-Jozsa 演算法
- ✓ 量子隱形傳態
- ✓ 量子相位估計

**執行方式：**
```bash
python example_04_quantum_algorithms.py
```

**學習重點：**
- 理解量子演算法的優勢
- 學習 oracle 的概念
- 體驗量子平行性

**演算法優勢：**
| 演算法 | 傳統方法 | 量子方法 |
|--------|----------|----------|
| Deutsch-Jozsa | O(2ⁿ) | O(1) |
| Bernstein-Vazirani | O(n) | O(1) |
| Grover 搜尋 | O(N) | O(√N) |

---

### 範例 5：實際應用 (`example_05_practical_applications.py`)

展示量子電路在實際場景中的應用。

**涵蓋內容：**
- ✓ 量子拋硬幣（公平隨機）
- ✓ 量子骰子（1-6）
- ✓ 量子樂透號碼生成器
- ✓ 量子密碼生成器
- ✓ 量子洗牌（撲克牌）
- ✓ 量子蒙地卡羅（估計 π）
- ✓ 量子遊戲 RNG（暴擊/掉寶）
- ✓ 量子決策器
- ✓ 量子加權選擇

**執行方式：**
```bash
python example_05_practical_applications.py
```

**學習重點：**
- 應用量子隨機性解決實際問題
- 理解真隨機與偽隨機的區別
- 創建自訂機率分布

**實用範例：**
```python
# 量子拋硬幣
result = quantum_coin_flip()  # "正面" 或 "反面"

# 量子骰子
number = quantum_dice()  # 1-6

# 量子密碼
password = quantum_password_generator(length=12)
```

---

## 🚀 快速開始

### 環境需求

```bash
pip install qiskit[all]
```

### 執行所有範例

```bash
# 範例 1：基本量子閘
python example_01_basic_gates.py

# 範例 2：量子糾纏
python example_02_entanglement.py

# 範例 3：疊加與干涉
python example_03_superposition_interference.py

# 範例 4：量子演算法
python example_04_quantum_algorithms.py

# 範例 5：實際應用
python example_05_practical_applications.py
```

---

## 📊 範例對照表

| 範例 | 難度 | 主題 | 適合對象 |
|------|------|------|----------|
| 01 | ⭐ | 基本量子閘 | 完全初學者 |
| 02 | ⭐⭐ | 量子糾纏 | 有基礎概念 |
| 03 | ⭐⭐⭐ | 疊加與干涉 | 理解量子力學 |
| 04 | ⭐⭐⭐⭐ | 量子演算法 | 有演算法背景 |
| 05 | ⭐⭐ | 實際應用 | 想要實作應用 |

---

## 🎯 學習路徑建議

### 初學者路徑
1. 先閱讀《量子電腦初學者教學.md》
2. 再閱讀《量子編程初學者教學.md》
3. 執行範例 1：理解基本量子閘
4. 執行範例 2：理解量子糾纏
5. 執行範例 5：體驗實際應用

### 進階路徑
1. 執行範例 3：深入理解干涉
2. 執行範例 4：學習量子演算法
3. 修改範例代碼，實驗不同參數
4. 嘗試組合不同技術創建新應用

---

## 📝 程式碼結構

所有範例都遵循相同的結構：

```python
# 1. 匯入模組
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

# 2. 創建量子電路
qc = QuantumCircuit(n_qubits, n_classical_bits)

# 3. 應用量子閘
qc.h(0)
qc.cx(0, 1)

# 4. 測量
qc.measure([0, 1], [0, 1])

# 5. 執行
sampler = Sampler()
job = sampler.run(qc, shots=1000)
result = job.result()

# 6. 獲取結果
counts = result.quasi_dists[0].binary_probabilities()

# 7. 儲存結果
with open("results.txt", "w", encoding="utf-8") as f:
    f.write(str(counts))
```

---

## 🔍 理解測量結果

### 結果格式

測量結果以字典形式返回：

```python
{'00': 0.501, '11': 0.499}
```

**解讀：**
- `'00'`：所有 qubits 都測量到 0
- `0.501`：這個結果出現的機率（50.1%）

### 常見模式

| 結果模式 | 說明 | 範例 |
|----------|------|------|
| `{'0': 0.5, '1': 0.5}` | 均等疊加態 | Hadamard 閘 |
| `{'0': 1.0}` | 確定狀態 \|0⟩ | 初始狀態 |
| `{'00': 0.5, '11': 0.5}` | 糾纏態 | 貝爾態 |
| `{'000': 0.125, ...}` | 多 qubit 疊加 | 多個 Hadamard |

---

## 💡 實驗建議

### 修改參數

每個範例都可以通過修改參數來實驗：

```python
# 修改 shots 數量
job = sampler.run(qc, shots=10000)  # 更準確的結果

# 修改旋轉角度
qc.ry(math.pi/3, 0)  # 嘗試不同角度

# 修改 qubit 數量
qc = QuantumCircuit(5, 5)  # 5 個 qubits
```

### 組合技術

嘗試組合不同的量子閘：

```python
# 組合範例：創建複雜的疊加態
qc = QuantumCircuit(2, 2)
qc.h(0)           # 疊加
qc.cx(0, 1)       # 糾纏
qc.ry(math.pi/4, 0)  # 旋轉
qc.measure([0, 1], [0, 1])
```

---

## 🐛 常見問題

### Q1: 為什麼結果每次都不同？

**A:** 量子測量是機率性的。使用更多的 shots 可以獲得更穩定的統計分布。

```python
# 少量 shots：結果波動大
job = sampler.run(qc, shots=10)

# 大量 shots：結果更穩定
job = sampler.run(qc, shots=10000)
```

### Q2: 如何確保結果的準確性？

**A:** 增加 shots 數量並多次運行：

```python
# 運行 10 次，取平均
results = []
for _ in range(10):
    job = sampler.run(qc, shots=1000)
    results.append(job.result().quasi_dists[0].binary_probabilities())
```

### Q3: 如何視覺化電路？

**A:** 使用 `draw()` 方法：

```python
# 文字格式
print(qc.draw())

# Matplotlib 圖形（需安裝 matplotlib）
qc.draw('mpl')
```

### Q4: 模擬器和真實量子電腦有什麼區別？

**A:**

| 特性 | 模擬器 | 真實量子電腦 |
|------|--------|--------------|
| 精確度 | 理想結果 | 有噪音和錯誤 |
| 速度 | 快速 | 需要排隊 |
| 限制 | 受記憶體限制 | qubit 數量少 |
| 成本 | 免費 | 有限的免費額度 |

---

## 📚 延伸學習

### 推薦資源

1. **官方文件**
   - [Qiskit 官方教學](https://qiskit.org/learn/)
   - [IBM Quantum Experience](https://quantum-computing.ibm.com/)

2. **進階主題**
   - 變分量子演算法（VQE、QAOA）
   - 量子機器學習
   - 量子錯誤修正
   - Grover 搜尋演算法
   - Shor 因數分解演算法

3. **實踐平台**
   - IBM Quantum Lab（線上 Jupyter 環境）
   - Qiskit Advocate 社群
   - 量子計算競賽和挑戰

### 下一步

完成這些範例後，您可以：

1. ✓ 嘗試實作 Grover 演算法
2. ✓ 探索量子機器學習
3. ✓ 連接到真實的量子電腦
4. ✓ 參加量子計算黑客松
5. ✓ 貢獻到 Qiskit 開源專案

---

## 🤝 貢獻

如果您有新的範例想法或改進建議：

1. 創建新的範例文件
2. 遵循現有的代碼結構
3. 添加詳細的註解和說明
4. 更新此 README

---

## 📄 授權

這些範例代碼可自由使用於學習和教學目的。

---

## 🎓 結語

量子計算是一個令人興奮的領域，這些範例只是一個開始。持續實驗、學習，您將逐漸掌握量子編程的精髓。

**記住：**
- 🧪 多實驗：改變參數，觀察結果
- 📖 多閱讀：理解背後的量子力學原理
- 💬 多交流：加入量子計算社群
- 🚀 多創造：用量子計算解決實際問題

**Happy Quantum Computing! 🎉**

---

## 📞 聯繫與支持

- Qiskit Slack: https://qiskit.slack.com/
- Stack Overflow: 使用 `qiskit` 標籤
- GitHub Issues: https://github.com/Qiskit/qiskit/issues

---

**版本：** 1.0
**最後更新：** 2025-11-13
**Qiskit 版本：** 1.0+
