# Ledger 硬件錢包技術教學

## 目錄
1. [簡介](#簡介)
2. [Ledger 硬件錢包概述](#ledger-硬件錢包概述)
3. [技術架構](#技術架構)
4. [安全機制](#安全機制)
5. [使用教學](#使用教學)
6. [開發者集成](#開發者集成)
7. [實踐範例](#實踐範例)
8. [常見問題](#常見問題)

---

## 簡介

### 什麼是硬件錢包？

硬件錢包是一種專門用於儲存加密貨幣私鑰的物理設備。與軟件錢包不同，硬件錢包將私鑰完全隔離在安全晶片中，即使連接到被感染的電腦也能保持安全。

### 為什麼選擇 Ledger？

Ledger 是全球領先的硬件錢包製造商，主要優勢包括：
- **安全晶片技術**：採用銀行級 CC EAL5+ 認證的安全元件
- **多幣種支援**：支援超過 5,500 種加密貨幣和代幣
- **開源生態**：部分代碼開源，接受社群審計
- **用戶友好**：簡潔直觀的操作界面

---

## Ledger 硬件錢包概述

### 主要產品線

#### 1. Ledger Nano S Plus
- **定位**：入門級硬件錢包
- **螢幕**：128×64 像素顯示屏
- **儲存**：可安裝 100+ 個應用程式
- **連接**：USB-C 連接
- **價格**：約 $79 USD

#### 2. Ledger Nano X
- **定位**：旗艦級移動錢包
- **螢幕**：128×64 像素顯示屏
- **儲存**：可安裝 100+ 個應用程式
- **連接**：USB-C + 藍牙
- **電池**：內建鋰電池，支援移動使用
- **價格**：約 $149 USD

#### 3. Ledger Stax
- **定位**：高端產品（2024年推出）
- **螢幕**：E Ink 觸控螢幕
- **設計**：由 iPod 設計師 Tony Fadell 設計
- **連接**：USB-C + 藍牙 + NFC
- **價格**：約 $279 USD

---

## 技術架構

### 硬件架構

```
┌─────────────────────────────────────────┐
│         Ledger 硬件錢包結構              │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   安全元件 (Secure Element)       │ │
│  │   - ST31/ST33 晶片                │ │
│  │   - CC EAL5+ 認證                 │ │
│  │   - 私鑰儲存                      │ │
│  │   - 加密運算                      │ │
│  └───────────────────────────────────┘ │
│              ↕                          │
│  ┌───────────────────────────────────┐ │
│  │   通用微控制器 (MCU)              │ │
│  │   - STM32 系列                    │ │
│  │   - 運行 BOLOS 作業系統           │ │
│  │   - 處理 UI 和通訊                │ │
│  └───────────────────────────────────┘ │
│              ↕                          │
│  ┌───────────────────────────────────┐ │
│  │   外設介面                        │ │
│  │   - USB/藍牙通訊                  │ │
│  │   - 顯示屏                        │ │
│  │   - 實體按鈕                      │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### BOLOS 作業系統

**BOLOS** (Blockchain Open Ledger Operating System) 是 Ledger 專門開發的作業系統：

#### 核心特性
1. **隔離執行環境**：每個應用程式在獨立環境中運行
2. **記憶體保護**：防止應用程式互相干擾
3. **安全啟動**：驗證固件完整性
4. **權限管理**：細粒度的 API 權限控制

#### 系統架構層次
```
┌──────────────────────────────────┐
│    應用層 (Apps)                 │
│  - Bitcoin App                   │
│  - Ethereum App                  │
│  - Custom Apps                   │
├──────────────────────────────────┤
│    BOLOS API                     │
│  - 密碼學 API                    │
│  - UI API                        │
│  - 儲存 API                      │
├──────────────────────────────────┤
│    BOLOS 核心                    │
│  - 任務調度                      │
│  - 記憶體管理                    │
│  - 安全監控                      │
├──────────────────────────────────┤
│    硬件抽象層 (HAL)              │
└──────────────────────────────────┘
```

### 軟件架構

#### Ledger Live
Ledger 的配套應用程式，提供：
- 資產管理界面
- 交易發送和接收
- 應用程式管理器
- 固件更新
- 質押和 DeFi 服務

#### 通訊協議
Ledger 使用 **APDU** (Application Protocol Data Unit) 協議與主機通訊：

```
指令 APDU 結構:
┌────┬────┬────┬────┬────┬──────────┐
│ CLA│ INS│ P1 │ P2 │ Lc │   Data   │
└────┴────┴────┴────┴────┴──────────┘
 1字節 1字節 1字節 1字節 1字節  變長

回應 APDU 結構:
┌──────────┬────┬────┐
│   Data   │ SW1│ SW2│
└──────────┴────┴────┘
   變長    1字節 1字節
```

---

## 安全機制

### 1. 安全元件 (Secure Element)

#### 特性
- **CC EAL5+ 認證**：通過國際通用準則認證
- **物理防護**：
  - 抗側信道攻擊
  - 抗故障注入攻擊
  - 抗電磁分析
- **真隨機數產生器 (TRNG)**：用於生成種子和密鑰

#### 安全晶片型號
- **ST31H320/ST31G480**：用於 Nano S
- **ST33J2M0**：用於 Nano X
- 銀行卡和護照也使用類似的晶片

### 2. 私鑰管理

#### BIP39 助記詞
Ledger 使用 BIP39 標準生成 24 字助記詞：

```
助記詞生成流程:
┌──────────────┐
│  生成熵值     │  256 位隨機數
│  (256 bits)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  計算校驗和   │  SHA256 前 8 位
│  (8 bits)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  轉換為單字   │  264 bits → 24 個單字
│  (24 words)  │  (每個單字 11 bits)
└──────────────┘
```

#### BIP32 分層確定性錢包
從助記詞派生所有私鑰：

```
助記詞 → 種子 (Seed)
           ↓
      主私鑰 (Master Key)
           ↓
    BIP32 路徑派生
           ↓
   m/44'/0'/0'/0/0  (Bitcoin)
   m/44'/60'/0'/0/0 (Ethereum)
   m/44'/...
```

#### BIP44 標準路徑
```
m / purpose' / coin_type' / account' / change / address_index

- purpose: 44' (BIP44)
- coin_type: 0' (Bitcoin), 60' (Ethereum), 等
- account: 帳戶索引
- change: 0 (接收地址), 1 (找零地址)
- address_index: 地址索引
```

### 3. 交易簽名流程

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   電腦/手機  │        │   Ledger    │         │  區塊鏈網絡  │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
       │ 1. 構建交易            │                       │
       │───────────────────────>│                       │
       │                       │                       │
       │                       │ 2. 顯示交易詳情       │
       │                       │    用戶確認           │
       │                       │                       │
       │ 3. 用戶按實體按鈕確認  │                       │
       │───────────────────────>│                       │
       │                       │                       │
       │                       │ 4. 在安全元件中簽名   │
       │                       │    (私鑰永不離開設備) │
       │                       │                       │
       │ 5. 返回簽名結果        │                       │
       │<───────────────────────│                       │
       │                       │                       │
       │ 6. 廣播已簽名交易      │                       │
       │───────────────────────────────────────────────>│
       │                       │                       │
```

### 4. PIN 碼保護

- **PIN 碼**：4-8 位數字
- **防暴力破解**：3 次錯誤後需重新插拔，連續錯誤後延遲增加
- **設備清除**：連續錯誤超過限制後自動清除數據

### 5. 可選密碼 (Passphrase)

BIP39 支援第 25 個單字（密碼短語）：
```
助記詞 + 密碼短語 → 完全不同的錢包
```

**用途**：
- 創建隱藏錢包
- 提供合理推諉性
- 額外的安全層

---

## 使用教學

### 初始設置

#### 步驟 1：開箱和檢查
```
✓ 檢查包裝是否完好無損
✓ 確認防拆貼紙完整
✓ 確認設備未被預先初始化
✓ 盒內包含：
  - Ledger 設備
  - USB 線
  - 恢復短語卡片
  - 鑰匙圈
  - 入門指南
```

#### 步驟 2：安裝 Ledger Live
1. 訪問官網：https://www.ledger.com/ledger-live
2. 下載適合您系統的版本（Windows/Mac/Linux）
3. 驗證下載檔案的 SHA256 校驗和
4. 安裝應用程式

#### 步驟 3：初始化設備
```python
# 初始化流程（在設備上操作）

1. 連接設備到電腦
2. 按實體按鈕開機
3. 選擇 "Set up as new device"
4. 選擇 PIN 碼（4-8 位數字）
   - 使用左右按鈕選擇數字
   - 同時按兩個按鈕確認
5. 確認 PIN 碼
6. 記錄 24 個助記詞
   - ⚠️ 永遠不要數位化儲存
   - ⚠️ 不要拍照
   - ⚠️ 使用提供的恢復卡片手寫記錄
7. 驗證助記詞
   - 按順序重新輸入單字確認
```

#### 步驟 4：配對 Ledger Live
```
1. 打開 Ledger Live
2. 選擇設備型號
3. 連接設備
4. 輸入 PIN 碼解鎖
5. 允許 Ledger 管理器
6. 完成配對
```

### 安裝應用程式

每種加密貨幣需要安裝對應的應用程式：

```
Ledger Live → Manager → 搜索應用程式 → Install

常用應用程式：
- Bitcoin (BTC)
- Ethereum (ETH)
- Bitcoin Cash (BCH)
- Litecoin (LTC)
- Polkadot (DOT)
- Cardano (ADA)
- Solana (SOL)
```

### 接收加密貨幣

```
流程：
1. Ledger Live → Accounts → [選擇帳戶]
2. 點擊 "Receive"
3. 選擇帳戶
4. 連接並解鎖 Ledger
5. 打開相應的應用程式（如 Bitcoin）
6. 在 Ledger 螢幕上驗證地址
   ⚠️ 確保 Ledger 顯示的地址與電腦螢幕一致
7. 複製地址或掃描 QR 碼
8. 發送資金到此地址
```

### 發送加密貨幣

```
流程：
1. Ledger Live → Accounts → [選擇帳戶]
2. 點擊 "Send"
3. 輸入：
   - 接收地址
   - 金額
   - 網絡費用（可調整）
4. 點擊 "Continue"
5. 在 Ledger 上確認：
   - 接收地址
   - 發送金額
   - 手續費
6. 按實體按鈕確認交易
7. 交易廣播到網絡
```

---

## 開發者集成

### Ledger 開發工具

#### 1. Ledger 開發環境
```bash
# 安裝開發工具
pip install ledgerblue

# 克隆開發 SDK
git clone https://github.com/LedgerHQ/ledger-app-builder

# 使用 Docker 構建環境
docker pull ghcr.io/ledgerhq/ledger-app-builder/ledger-app-builder:latest
```

#### 2. 開發語言
- **C 語言**：用於開發 Ledger 應用程式
- **Python**：用於測試和與設備通訊
- **JavaScript/TypeScript**：用於 Web 集成

### 開發自定義應用程式

#### 應用程式結構
```
ledger-app-myapp/
├── src/
│   ├── main.c           # 主程式入口
│   ├── ui.c             # 用戶介面
│   ├── crypto.c         # 加密運算
│   └── handlers.c       # APDU 處理
├── glyphs/              # 圖標資源
├── Makefile             # 構建配置
└── README.md
```

#### 基本應用程式範例
```c
// main.c
#include "os.h"
#include "cx.h"
#include "ux.h"

// 全局 APDU 緩衝區
unsigned char G_io_apdu_buffer[IO_APDU_BUFFER_SIZE];

// 處理 GET_VERSION 指令
void handleGetVersion() {
    G_io_apdu_buffer[0] = 0x01;  // 主版本
    G_io_apdu_buffer[1] = 0x00;  // 次版本
    G_io_apdu_buffer[2] = 0x00;  // 補丁版本

    io_exchange_with_code(0x9000, 3);  // 返回成功
}

// 處理 GET_PUBLIC_KEY 指令
void handleGetPublicKey() {
    uint8_t privateKeyData[32];
    cx_ecfp_private_key_t privateKey;
    cx_ecfp_public_key_t publicKey;

    // 從 BIP32 路徑派生私鑰
    os_perso_derive_node_bip32(
        CX_CURVE_256K1,
        derivationPath,
        derivationPathLength,
        privateKeyData,
        NULL
    );

    // 初始化私鑰
    cx_ecfp_init_private_key(
        CX_CURVE_256K1,
        privateKeyData,
        32,
        &privateKey
    );

    // 生成公鑰
    cx_ecfp_generate_pair(
        CX_CURVE_256K1,
        &publicKey,
        &privateKey,
        1
    );

    // 返回公鑰
    os_memmove(G_io_apdu_buffer, publicKey.W, 65);
    io_exchange_with_code(0x9000, 65);
}

// 主 APDU 處理函數
void handleApdu(unsigned int *flags) {
    unsigned short sw = 0;

    switch (G_io_apdu_buffer[1]) {  // INS 字節
        case 0x00:  // GET_VERSION
            handleGetVersion();
            break;

        case 0x01:  // GET_PUBLIC_KEY
            handleGetPublicKey();
            break;

        case 0x02:  // SIGN_TRANSACTION
            handleSignTransaction();
            break;

        default:
            THROW(0x6D00);  // INS not supported
            break;
    }
}
```

### Web 集成

#### 使用 @ledgerhq/hw-transport-webusb
```javascript
// 安裝依賴
// npm install @ledgerhq/hw-transport-webusb
// npm install @ledgerhq/hw-app-eth

import TransportWebUSB from "@ledgerhq/hw-transport-webusb";
import Eth from "@ledgerhq/hw-app-eth";

// 連接到 Ledger
async function connectLedger() {
    try {
        // 請求 USB 連接
        const transport = await TransportWebUSB.create();

        // 創建 Ethereum 應用實例
        const eth = new Eth(transport);

        return eth;
    } catch (error) {
        console.error("連接失敗:", error);
        throw error;
    }
}

// 獲取 Ethereum 地址
async function getAddress() {
    const eth = await connectLedger();

    // BIP44 路徑: m/44'/60'/0'/0/0
    const path = "44'/60'/0'/0/0";

    const result = await eth.getAddress(path, true);  // true = 在設備上顯示

    console.log("地址:", result.address);
    console.log("公鑰:", result.publicKey);

    return result.address;
}

// 簽名交易
async function signTransaction() {
    const eth = await connectLedger();

    // 交易數據（RLP 編碼的原始交易）
    const txData = {
        nonce: "0x00",
        gasPrice: "0x3b9aca00",  // 1 Gwei
        gasLimit: "0x5208",       // 21000
        to: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        value: "0x0de0b6b3a7640000",  // 1 ETH
        data: "0x",
        chainId: 1  // 主網
    };

    // 序列化交易
    const serializedTx = serializeTransaction(txData);

    // 簽名
    const signature = await eth.signTransaction(
        "44'/60'/0'/0/0",
        serializedTx
    );

    console.log("簽名結果:", signature);
    return signature;
}

// 輔助函數：序列化交易
function serializeTransaction(tx) {
    // 使用 ethers.js 或 web3.js 序列化
    const ethers = require('ethers');

    const transaction = {
        nonce: tx.nonce,
        gasPrice: tx.gasPrice,
        gasLimit: tx.gasLimit,
        to: tx.to,
        value: tx.value,
        data: tx.data,
        chainId: tx.chainId
    };

    return ethers.utils.serializeTransaction(transaction);
}
```

#### 使用 Ledger Live SDK
```javascript
// 安裝
// npm install @ledgerhq/live-common

import { fromAccountRaw } from "@ledgerhq/live-common/account";
import { getAccountBridge } from "@ledgerhq/live-common/bridge";

async function sendTransaction(account, recipient, amount) {
    // 獲取帳戶橋接器
    const bridge = getAccountBridge(account);

    // 準備交易
    let transaction = bridge.createTransaction(account);

    transaction = bridge.updateTransaction(transaction, {
        recipient: recipient,
        amount: amount
    });

    // 準備交易（計算費用等）
    transaction = await bridge.prepareTransaction(account, transaction);

    // 簽名交易（需要 Ledger 設備確認）
    const signedOperation = await bridge.signOperation({
        account: account,
        transaction: transaction,
        deviceId: "ledger-device-id"
    });

    // 廣播交易
    const optimisticOperation = signedOperation.optimisticOperation;
    const operation = await bridge.broadcast({
        account: account,
        signedOperation: signedOperation
    });

    return operation;
}
```

### Python 集成

```python
# 安裝: pip install ledgerblue

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException

class LedgerWallet:
    def __init__(self):
        self.dongle = None

    def connect(self):
        """連接到 Ledger 設備"""
        try:
            self.dongle = getDongle(True)
            print("已連接到 Ledger")
            return True
        except CommException as e:
            print(f"連接失敗: {e}")
            return False

    def send_apdu(self, cla, ins, p1, p2, data=b""):
        """發送 APDU 指令"""
        if not self.dongle:
            raise Exception("未連接到設備")

        # 構建 APDU
        apdu = bytes([cla, ins, p1, p2, len(data)]) + data

        try:
            # 發送並接收回應
            response = self.dongle.exchange(apdu)

            # 檢查狀態碼
            sw = (response[-2] << 8) | response[-1]
            if sw != 0x9000:
                raise Exception(f"錯誤: 0x{sw:04x}")

            return response[:-2]
        except CommException as e:
            raise Exception(f"通訊錯誤: {e}")

    def get_public_key(self, path="44'/0'/0'/0/0"):
        """獲取公鑰"""
        # 解析 BIP32 路徑
        path_elements = [int(x.replace("'", "")) | 0x80000000
                        if "'" in x else int(x)
                        for x in path.split("/")]

        # 構建路徑數據
        path_data = bytes([len(path_elements)])
        for element in path_elements:
            path_data += element.to_bytes(4, 'big')

        # 發送 GET_PUBLIC_KEY 指令
        response = self.send_apdu(
            cla=0xE0,
            ins=0x02,
            p1=0x00,
            p2=0x00,
            data=path_data
        )

        # 解析回應
        public_key_length = response[0]
        public_key = response[1:1+public_key_length]

        return public_key.hex()

    def close(self):
        """關閉連接"""
        if self.dongle:
            self.dongle.close()
            print("連接已關閉")

# 使用範例
if __name__ == "__main__":
    wallet = LedgerWallet()

    if wallet.connect():
        try:
            # 獲取 Bitcoin 主地址的公鑰
            pubkey = wallet.get_public_key("44'/0'/0'/0/0")
            print(f"公鑰: {pubkey}")
        except Exception as e:
            print(f"錯誤: {e}")
        finally:
            wallet.close()
```

---

## 實踐範例

### 範例 1：Bitcoin 交易簽名

```python
from ledgerblue.comm import getDongle
import hashlib

def sign_bitcoin_transaction(inputs, outputs, change_address):
    """
    簽名 Bitcoin 交易

    Args:
        inputs: 輸入列表 [{txid, vout, amount, address}]
        outputs: 輸出列表 [{address, amount}]
        change_address: 找零地址
    """
    dongle = getDongle(True)

    # 1. 構建交易
    tx = build_transaction(inputs, outputs, change_address)

    # 2. 為每個輸入簽名
    signatures = []
    for i, inp in enumerate(inputs):
        # 獲取輸入的派生路徑
        path = inp['path']

        # 構建簽名哈希
        sighash = create_sighash(tx, i)

        # 發送簽名請求到 Ledger
        apdu = build_sign_apdu(path, sighash)
        response = dongle.exchange(apdu)

        # 解析簽名
        signature = parse_signature(response)
        signatures.append(signature)

    # 3. 構建完整交易
    signed_tx = finalize_transaction(tx, signatures)

    dongle.close()
    return signed_tx

def build_transaction(inputs, outputs, change_address):
    """構建未簽名交易"""
    tx = {
        'version': 2,
        'inputs': [],
        'outputs': [],
        'locktime': 0
    }

    # 添加輸入
    for inp in inputs:
        tx['inputs'].append({
            'txid': bytes.fromhex(inp['txid'])[::-1],
            'vout': inp['vout'],
            'script': b'',
            'sequence': 0xfffffffe
        })

    # 計算總輸入金額
    total_input = sum(inp['amount'] for inp in inputs)
    total_output = sum(out['amount'] for out in outputs)
    fee = 10000  # 0.0001 BTC
    change = total_input - total_output - fee

    # 添加輸出
    for out in outputs:
        tx['outputs'].append({
            'amount': out['amount'],
            'script': address_to_script(out['address'])
        })

    # 添加找零輸出
    if change > 0:
        tx['outputs'].append({
            'amount': change,
            'script': address_to_script(change_address)
        })

    return tx
```

### 範例 2：Ethereum DApp 集成

```javascript
// React Hook 用於 Ledger 集成
import { useState, useEffect } from 'react';
import TransportWebUSB from "@ledgerhq/hw-transport-webusb";
import Eth from "@ledgerhq/hw-app-eth";
import { ethers } from 'ethers';

export function useLedger() {
    const [transport, setTransport] = useState(null);
    const [eth, setEth] = useState(null);
    const [address, setAddress] = useState(null);
    const [isConnected, setIsConnected] = useState(false);

    // 連接 Ledger
    const connect = async () => {
        try {
            const t = await TransportWebUSB.create();
            const e = new Eth(t);

            setTransport(t);
            setEth(e);
            setIsConnected(true);

            // 獲取預設地址
            const result = await e.getAddress("44'/60'/0'/0/0");
            setAddress(result.address);

            return result.address;
        } catch (error) {
            console.error("連接失敗:", error);
            throw error;
        }
    };

    // 斷開連接
    const disconnect = async () => {
        if (transport) {
            await transport.close();
            setTransport(null);
            setEth(null);
            setAddress(null);
            setIsConnected(false);
        }
    };

    // 簽名交易
    const signTransaction = async (txParams) => {
        if (!eth) throw new Error("未連接");

        // 構建交易
        const tx = {
            to: txParams.to,
            value: ethers.utils.parseEther(txParams.value).toHexString(),
            gasLimit: ethers.utils.hexlify(21000),
            gasPrice: ethers.utils.parseUnits('50', 'gwei').toHexString(),
            nonce: ethers.utils.hexlify(txParams.nonce),
            chainId: 1,
            data: '0x'
        };

        // 序列化交易
        const serializedTx = ethers.utils.serializeTransaction(tx).slice(2);

        // 使用 Ledger 簽名
        const signature = await eth.signTransaction(
            "44'/60'/0'/0/0",
            serializedTx
        );

        // 構建完整簽名
        const fullSignature = {
            r: '0x' + signature.r,
            s: '0x' + signature.s,
            v: parseInt(signature.v, 10)
        };

        // 組合簽名後的交易
        const signedTx = ethers.utils.serializeTransaction(tx, fullSignature);

        return signedTx;
    };

    // 簽名消息
    const signMessage = async (message) => {
        if (!eth) throw new Error("未連接");

        const result = await eth.signPersonalMessage(
            "44'/60'/0'/0/0",
            Buffer.from(message).toString('hex')
        );

        return {
            r: '0x' + result.r,
            s: '0x' + result.s,
            v: result.v
        };
    };

    return {
        address,
        isConnected,
        connect,
        disconnect,
        signTransaction,
        signMessage
    };
}

// 使用範例組件
function LedgerWalletComponent() {
    const {
        address,
        isConnected,
        connect,
        disconnect,
        signTransaction
    } = useLedger();

    const handleSendTransaction = async () => {
        try {
            const signedTx = await signTransaction({
                to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
                value: '0.1',
                nonce: 0
            });

            // 廣播交易
            const provider = new ethers.providers.JsonRpcProvider(RPC_URL);
            const txResponse = await provider.sendTransaction(signedTx);

            console.log('交易哈希:', txResponse.hash);
            await txResponse.wait();
            console.log('交易確認');
        } catch (error) {
            console.error('交易失敗:', error);
        }
    };

    return (
        <div>
            {!isConnected ? (
                <button onClick={connect}>連接 Ledger</button>
            ) : (
                <>
                    <p>地址: {address}</p>
                    <button onClick={handleSendTransaction}>
                        發送交易
                    </button>
                    <button onClick={disconnect}>
                        斷開連接
                    </button>
                </>
            )}
        </div>
    );
}
```

### 範例 3：多重簽名錢包集成

```javascript
// Gnosis Safe 與 Ledger 集成
import Safe from '@safe-global/safe-core-sdk';
import EthersAdapter from '@safe-global/safe-ethers-lib';
import { ethers } from 'ethers';

class LedgerSafeIntegration {
    constructor() {
        this.eth = null;
        this.safe = null;
    }

    async initialize(safeAddress, ledgerPath = "44'/60'/0'/0/0") {
        // 連接 Ledger
        const transport = await TransportWebUSB.create();
        this.eth = new Eth(transport);

        // 創建 Ledger Signer
        const ledgerSigner = new LedgerSigner(this.eth, ledgerPath);

        // 初始化 Safe SDK
        const ethAdapter = new EthersAdapter({
            ethers,
            signerOrProvider: ledgerSigner
        });

        this.safe = await Safe.create({
            ethAdapter,
            safeAddress
        });
    }

    async proposeTransaction(to, value, data) {
        // 創建交易
        const safeTransaction = await this.safe.createTransaction({
            safeTransactionData: {
                to,
                value,
                data
            }
        });

        // 使用 Ledger 簽名
        const signedTx = await this.safe.signTransaction(safeTransaction);

        return signedTx;
    }

    async executeTransaction(safeTransaction) {
        // 執行交易（需要足夠的簽名）
        const executeTxResponse = await this.safe.executeTransaction(
            safeTransaction
        );

        await executeTxResponse.transactionResponse.wait();

        return executeTxResponse.hash;
    }
}

// Ledger Signer 類
class LedgerSigner extends ethers.Signer {
    constructor(eth, path) {
        super();
        this.eth = eth;
        this.path = path;
        this.address = null;
    }

    async getAddress() {
        if (!this.address) {
            const result = await this.eth.getAddress(this.path);
            this.address = result.address;
        }
        return this.address;
    }

    async signMessage(message) {
        const messageHex = Buffer.from(message).toString('hex');
        const result = await this.eth.signPersonalMessage(
            this.path,
            messageHex
        );

        return ethers.utils.joinSignature({
            r: '0x' + result.r,
            s: '0x' + result.s,
            v: result.v
        });
    }

    async signTransaction(transaction) {
        const unsignedTx = ethers.utils.serializeTransaction(transaction);
        const signature = await this.eth.signTransaction(
            this.path,
            unsignedTx.slice(2)
        );

        return ethers.utils.serializeTransaction(transaction, {
            r: '0x' + signature.r,
            s: '0x' + signature.s,
            v: signature.v
        });
    }

    connect(provider) {
        return new LedgerSigner(this.eth, this.path).connectUnchecked(provider);
    }
}
```

---

## 常見問題

### 安全相關

**Q: 如果遺失了 Ledger 設備怎麼辦？**
A: 只要保管好 24 字助記詞，就可以在新的 Ledger 或任何支援 BIP39 的錢包中恢復。

**Q: 助記詞可以數位化儲存嗎？**
A: 強烈不建議。應該：
- 手寫在紙上
- 使用金屬備份板（防火防水）
- 考慮使用 Cryptosteel 等專業解決方案
- 絕不拍照或存在電腦/雲端

**Q: Ledger 可以被駭客攻擊嗎？**
A: 理論上私鑰在安全元件中是安全的，但要注意：
- 供應鏈攻擊（購買全新且密封的設備）
- 網路釣魚（確認交易細節）
- 物理攻擊（保管好設備）

**Q: 什麼是可選密碼（Passphrase）？**
A: BIP39 的第 25 個單字，可以：
- 創建隱藏錢包
- 提供合理推諉性
- 但如果忘記密碼，資金將永遠無法恢復

### 使用相關

**Q: 為什麼每次使用都要輸入 PIN 碼？**
A: 這是安全設計，確保即使設備被盜也無法使用。

**Q: 可以在多台電腦上使用同一個 Ledger 嗎？**
A: 可以，Ledger 設備本身儲存所有必要信息，可以在任何電腦上使用。

**Q: Ledger Live 必須使用嗎？**
A: 不是，可以使用其他支援硬件錢包的應用：
- MetaMask
- MyEtherWallet
- Electrum
- Sparrow Wallet

**Q: 為什麼交易費用這麼高？**
A: 費用由區塊鏈網絡決定，Ledger 不收取交易費。可以在發送前調整費用。

### 技術相關

**Q: Ledger 支援哪些區塊鏈？**
A: 支援 5,500+ 種資產，包括：
- Bitcoin 及分叉幣
- Ethereum 及 ERC-20 代幣
- Solana、Cardano、Polkadot
- BSC、Polygon 等 L2/側鏈

**Q: 可以在一個 Ledger 上管理多個錢包嗎？**
A: 可以通過：
1. 不同的帳戶索引（BIP44）
2. 可選密碼創建完全獨立的錢包

**Q: ERC-20 代幣需要安裝額外應用嗎？**
A: 不需要，所有 ERC-20 代幣使用 Ethereum 應用程式。

**Q: Ledger 開源嗎？**
A: 部分開源：
- Ledger Live：開源
- 應用程式代碼：大部分開源
- BOLOS 和固件：閉源（但經過審計）

### 故障排除

**Q: 無法連接到 Ledger Live**
A: 檢查：
1. USB 線是否正常
2. 是否安裝了最新的 Ledger Live
3. 防火牆設置
4. 嘗試不同的 USB 端口
5. 關閉其他可能占用設備的應用

**Q: 交易卡住/未確認**
A:
- Bitcoin：可以使用 RBF (Replace-By-Fee) 加速
- Ethereum：可以發送相同 nonce 的交易覆蓋

**Q: 固件更新失敗**
A:
1. 確保電量充足（Nano X）
2. 使用官方 USB 線
3. 重試前關閉所有加密貨幣應用
4. 聯繫 Ledger 支援

---

## 進階主題

### 1. 自定義派生路徑

```javascript
// 使用非標準路徑
const customPath = "44'/60'/0'/0/100";  // 第 100 個地址
const result = await eth.getAddress(customPath);
```

### 2. 批次地址生成

```python
def generate_addresses(start_index, count):
    """生成多個地址"""
    dongle = getDongle(True)
    addresses = []

    for i in range(start_index, start_index + count):
        path = f"44'/0'/0'/0/{i}"
        pubkey = get_public_key(dongle, path)
        address = pubkey_to_address(pubkey)
        addresses.append({
            'index': i,
            'path': path,
            'address': address
        })

    dongle.close()
    return addresses
```

### 3. 冷錢包設置

將 Ledger 作為完全離線的冷錢包：
```
1. 使用 Ledger 生成地址（在線）
2. 記錄地址後斷開設備
3. 在線電腦構建未簽名交易
4. 通過 QR 碼或 USB 傳輸到離線電腦
5. 在離線電腦上使用 Ledger 簽名
6. 傳回已簽名交易
7. 在線電腦廣播交易
```

### 4. 與 DeFi 協議集成

```javascript
// Uniswap 交易範例
async function swapWithLedger(tokenIn, tokenOut, amount) {
    const eth = await connectLedger();

    // 構建 Uniswap 交易數據
    const swapData = uniswapRouter.interface.encodeFunctionData(
        'swapExactTokensForTokens',
        [amount, minAmountOut, [tokenIn, tokenOut], address, deadline]
    );

    // 簽名交易
    const signedTx = await signTransactionWithLedger(eth, {
        to: UNISWAP_ROUTER_ADDRESS,
        value: '0',
        data: swapData
    });

    return signedTx;
}
```

---

## 最佳實踐

### 安全檢查清單

- [ ] 僅從官方渠道購買設備
- [ ] 檢查防拆封標籤
- [ ] 手寫備份助記詞
- [ ] 在多個安全地點備份
- [ ] 驗證接收地址
- [ ] 在 Ledger 屏幕上確認交易細節
- [ ] 定期更新固件
- [ ] 使用強 PIN 碼
- [ ] 考慮使用可選密碼
- [ ] 測試恢復流程

### 開發檢查清單

- [ ] 驗證交易數據格式
- [ ] 實現錯誤處理
- [ ] 提供清晰的用戶提示
- [ ] 在設備上顯示完整交易信息
- [ ] 測試各種錯誤情況
- [ ] 實現重試邏輯
- [ ] 記錄用戶操作
- [ ] 遵守 Ledger 開發指南
- [ ] 進行安全審計
- [ ] 提供完整的文檔

---

## 資源鏈接

### 官方資源
- 官網: https://www.ledger.com
- Ledger Live: https://www.ledger.com/ledger-live
- 開發者文檔: https://developers.ledger.com
- GitHub: https://github.com/LedgerHQ

### 學習資源
- Ledger Academy: https://www.ledger.com/academy
- Developer Portal: https://developers.ledger.com/docs/
- App Development Guide: https://developers.ledger.com/docs/nano-app/

### 社群
- Reddit: r/ledgerwallet
- Discord: https://discord.gg/ledger
- Twitter: @Ledger

### 工具庫
- @ledgerhq/hw-transport-webusb
- @ledgerhq/hw-app-eth
- @ledgerhq/hw-app-btc
- ledgerblue (Python)

---

## 結語

Ledger 硬件錢包是保護加密資產最安全的方式之一。通過結合安全元件技術、BOLOS 作業系統、以及用戶友好的設計，Ledger 為用戶提供了既安全又便捷的加密貨幣管理方案。

對於開發者，Ledger 提供了完整的開發工具和 API，可以輕鬆將硬件錢包集成到應用程式中，為用戶提供更高的安全保障。

記住：**不是你的私鑰，就不是你的幣。** 使用硬件錢包是真正掌控自己資產的第一步。

---

**最後更新**: 2024年11月
**版本**: 1.0
**作者**: Ledger 技術教學團隊
