# Trezor 硬件錢包技術教學

## 目錄
1. [簡介](#簡介)
2. [Trezor 硬件錢包概述](#trezor-硬件錢包概述)
3. [核心技術原理](#核心技術原理)
4. [安全機制](#安全機制)
5. [Trezor 產品線](#trezor-產品線)
6. [使用指南](#使用指南)
7. [開發者指南](#開發者指南)
8. [常見問題](#常見問題)
9. [總結](#總結)

---

## 簡介

Trezor 是世界上第一個比特幣硬件錢包，由 SatoshiLabs 於 2014 年推出。它提供了一種安全的方式來存儲加密貨幣私鑰，通過將私鑰離線存儲來保護用戶的數字資產免受黑客攻擊。

### 什麼是硬件錢包？

硬件錢包是一種物理電子設備，專門用於安全地存儲加密貨幣私鑰。與軟件錢包不同，硬件錢包將私鑰保存在設備內部，永不暴露給連接的計算機或網絡，從而大大提高了安全性。

---

## Trezor 硬件錢包概述

### 主要特點

1. **離線存儲**：私鑰永遠不會離開設備
2. **PIN 碼保護**：防止物理訪問時的未授權使用
3. **恢復種子**：24 個單詞的助記詞用於備份和恢復
4. **開源**：硬件和軟件都是開源的，可供社區審查
5. **多幣種支持**：支持數千種加密貨幣和代幣
6. **用戶友好**：簡潔的界面和清晰的操作流程

### 適用場景

- 長期持有大量加密貨幣
- 需要最高級別安全保護的用戶
- 多種加密貨幣的管理
- 企業級數字資產管理

---

## 核心技術原理

### 1. 分層確定性錢包 (HD Wallet)

Trezor 使用 BIP32、BIP39 和 BIP44 標準實現分層確定性錢包：

#### BIP39 - 助記詞
```
工作原理：
1. 生成 128-256 位的隨機熵
2. 添加校驗和
3. 將結果分割為 12-24 個單詞
4. 使用標準化的 2048 個單詞列表
```

示例助記詞（請勿在實際使用中使用此示例）：
```
witch collapse practice feed shame open despair creek road again ice least
```

#### BIP32 - 分層確定性
```
主種子 (Master Seed)
    |
    ├─ m/44'/0'/0'  (Bitcoin)
    |     |
    |     ├─ m/44'/0'/0'/0/0  (第一個接收地址)
    |     ├─ m/44'/0'/0'/0/1  (第二個接收地址)
    |     └─ m/44'/0'/0'/1/0  (第一個找零地址)
    |
    ├─ m/44'/60'/0' (Ethereum)
    |     └─ m/44'/60'/0'/0/0
    |
    └─ m/44'/2'/0'  (Litecoin)
```

#### BIP44 - 多幣種層次結構
```
m / purpose' / coin_type' / account' / change / address_index

參數說明：
- purpose: 固定為 44'（表示 BIP44）
- coin_type: 幣種類型（0'=BTC, 60'=ETH, 2'=LTC）
- account: 帳戶索引（從 0' 開始）
- change: 0=外部鏈（接收），1=內部鏈（找零）
- address_index: 地址索引（從 0 開始）
```

### 2. 加密技術

#### 橢圓曲線加密 (ECC)

Trezor 使用 secp256k1 曲線（比特幣標準）：

```python
# 偽代碼示例
私鑰 = 隨機生成的 256 位數字
公鑰 = 私鑰 × G（生成點）
地址 = Hash(公鑰)
```

關鍵特性：
- 私鑰範圍：1 到 n-1（其中 n ≈ 2^256）
- 公鑰是橢圓曲線上的點 (x, y)
- 簽名算法：ECDSA (Elliptic Curve Digital Signature Algorithm)

#### 哈希函數

Trezor 使用多種哈希函數：

```
SHA-256: 用於比特幣地址生成
RIPEMD-160: 與 SHA-256 組合使用
Keccak-256: 用於以太坊地址
PBKDF2: 用於助記詞到種子的轉換
```

### 3. 交易簽名流程

```
步驟 1: 計算機創建未簽名交易
    ↓
步驟 2: 交易數據發送到 Trezor
    ↓
步驟 3: Trezor 屏幕顯示交易詳情
    ↓
步驟 4: 用戶在 Trezor 上確認
    ↓
步驟 5: Trezor 使用私鑰簽名交易
    ↓
步驟 6: 簽名後的交易返回計算機
    ↓
步驟 7: 計算機廣播交易到網絡
```

關鍵點：**私鑰永遠不離開 Trezor 設備**

---

## 安全機制

### 1. 硬件安全

#### 安全元件
```
Trezor Model One:
- STM32F205 微控制器
- 無專用安全芯片
- 依賴固件和物理設計

Trezor Model T:
- STM32F427 微控制器
- 觸摸屏界面
- 增強的物理安全設計
```

#### 防篡改設計
- 超聲波焊接外殼
- 檢測物理入侵的機制
- 固件簽名驗證

### 2. PIN 碼保護

#### 盲輸入機制
```
設備屏幕顯示：        計算機屏幕顯示：
┌───┬───┬───┐        ┌───┬───┬───┐
│ 6 │ 2 │ 8 │        │ • │ • │ • │
├───┼───┼───┤        ├───┼───┼───┤
│ 5 │ 9 │ 1 │        │ • │ • │ • │
├───┼───┼───┤        ├───┼───┼───┤
│ 4 │ 7 │ 3 │        │ • │ • │ • │
└───┴───┴───┘        └───┴───┴───┘
```

特點：
- 數字佈局每次隨機
- 計算機只知道點擊位置，不知道數字
- 防鍵盤記錄器攻擊

#### PIN 碼失敗懲罰
```
失敗次數    等待時間
1-2         無
3           2^2 秒
4           2^3 秒
5           2^4 秒
...
16+         2^15 秒（約 9 小時）
```

### 3. 密碼短語 (Passphrase)

額外的安全層：

```
助記詞 + 密碼短語 = 唯一的種子

例如：
助記詞: "witch collapse practice..."
密碼短語: "MySecretPassphrase123"
結果: 完全不同的錢包地址集
```

優勢：
- 隱藏錢包（plausible deniability）
- 即使助記詞被盜，沒有密碼短語也無法訪問
- 可創建多個隱藏錢包

### 4. 固件安全

#### 啟動載入程序 (Bootloader)
```
啟動流程：
1. Bootloader 檢查固件簽名
2. 驗證 SatoshiLabs 的數字簽名
3. 用戶確認固件指紋
4. 加載固件
```

#### 固件更新
- 必須手動確認
- 會清除設備存儲（安全措施）
- 需要從助記詞恢復

### 5. 通信安全

#### USB 通信協議
```
Protocol Buffers 格式：
message ApplySettings {
    optional string language = 1;
    optional string label = 2;
    optional bool use_passphrase = 3;
    optional bytes homescreen = 4;
}
```

加密通信：
- 使用 AES-256 加密敏感數據
- ECDH 密鑰交換
- 防止中間人攻擊

---

## Trezor 產品線

### Trezor Model One

**規格：**
- 處理器：120 MHz ARM Cortex-M3
- 屏幕：128×64 OLED
- 連接：Micro USB
- 輸入：2 個物理按鈕
- 重量：12 克

**優勢：**
- 價格較低（約 $69）
- 久經考驗的設計
- 社區廣泛支持

**限制：**
- 不支持某些新幣種（如 Cardano、Monero）
- 無觸摸屏

### Trezor Model T

**規格：**
- 處理器：168 MHz ARM Cortex-M4
- 屏幕：240×240 LCD 彩色觸摸屏
- 連接：USB-C
- 輸入：觸摸屏
- SD 卡槽：支持加密存儲
- 重量：22 克

**優勢：**
- 觸摸屏輸入（更安全的 PIN 輸入）
- 支持更多幣種
- Shamir 備份（SLIP39）
- 更大的彩色屏幕

**價格：** 約 $219

### 功能對比

| 功能 | Model One | Model T |
|------|-----------|---------|
| 支持幣種 | 1000+ | 1450+ |
| 觸摸屏 | ❌ | ✅ |
| Shamir 備份 | ❌ | ✅ |
| SD 卡加密 | ❌ | ✅ |
| U2F 認證 | ✅ | ✅ |
| 密碼管理器 | ✅ | ✅ |
| 開源 | ✅ | ✅ |

---

## 使用指南

### 初始設置

#### 1. 開箱檢查
```
✓ 檢查包裝密封完整
✓ 驗證全息貼紙
✓ 確保設備未被開啟過
✓ 檢查包裝內容：
  - Trezor 設備
  - USB 線
  - 恢復種子卡
  - 用戶手冊
```

#### 2. 安裝 Trezor Suite

訪問 trezor.io/start 下載官方軟件：

```bash
# Linux 安裝（示例）
wget https://suite.trezor.io/web/static/desktop/Trezor-Suite-24.x.x-linux-x86_64.AppImage
chmod +x Trezor-Suite-24.x.x-linux-x86_64.AppImage
./Trezor-Suite-24.x.x-linux-x86_64.AppImage

# macOS
# 下載 .dmg 文件並安裝

# Windows
# 下載 .exe 安裝程序
```

#### 3. 創建新錢包

```
步驟流程：
1. 連接 Trezor 到計算機
2. 選擇 "Create new wallet"
3. 設置設備名稱
4. 設置 PIN 碼（4-50 位數字）
5. 記錄恢復種子（12 或 24 個單詞）
6. 驗證恢復種子
7. 完成設置
```

**⚠️ 重要安全提示：**
```
✓ 在離線環境記錄助記詞
✓ 使用防水防火的存儲方式
✓ 永遠不要拍照或電子存儲
✓ 考慮使用金屬備份板
✓ 多地點備份
✓ 永遠不要與任何人分享
```

#### 4. 恢復種子備份最佳實踐

```
方法 1: 紙質備份
- 使用隨附的恢復卡
- 清晰書寫
- 多份副本（3+）
- 分別存放

方法 2: 金屬備份（推薦）
- 耐火（1000°C+）
- 耐水
- 耐腐蝕
- 產品：Cryptosteel、Billfodl

方法 3: Shamir 備份（僅 Model T）
- 將種子分成多份（如 5 份）
- 設置恢復閾值（如需要 3 份）
- 更高的安全性和靈活性
```

### 日常使用

#### 接收加密貨幣

```python
# 偽代碼流程
1. 打開 Trezor Suite
2. 選擇對應的幣種賬戶
3. 點擊 "Receive"
4. 在 Trezor 設備上確認地址
5. 複製地址或顯示 QR 碼
6. 發送給付款方
```

**安全檢查清單：**
- ✓ 始終在 Trezor 屏幕上驗證地址
- ✓ 小額測試交易
- ✓ 檢查地址格式正確性

#### 發送加密貨幣

```
流程：
1. 在 Suite 中點擊 "Send"
2. 輸入接收地址
3. 輸入發送金額
4. 設置手續費（慢/正常/快）
5. 檢查交易詳情
6. 在 Trezor 設備上確認：
   - 接收地址
   - 發送金額
   - 手續費
7. 物理按鈕確認
8. 交易廣播到網絡
```

#### 手續費設置

```
比特幣手續費估算：

低優先級：1-5 sat/vB
  時間：1-24 小時
  成本：低

中優先級：5-20 sat/vB
  時間：10-60 分鐘
  成本：中

高優先級：20+ sat/vB
  時間：0-10 分鐘
  成本：高
```

### 高級功能

#### 1. 密碼短語使用

```
啟用流程：
設置 → Advanced → Passphrase → Enable

使用場景：
標準錢包：無密碼短語（日常小額）
隱藏錢包 1：密碼短語 "Business2024"（商用）
隱藏錢包 2：密碼短語 "Investment#001"（投資）

⚠️ 注意：
- 忘記密碼短語 = 永久失去訪問權限
- 密碼短語無法恢復
- 建議安全記錄
```

#### 2. 多簽名錢包

```
配置示例（2-of-3 多簽）：

設備：
- Trezor 1（你的）
- Trezor 2（合作夥伴 A）
- Trezor 3（合作夥伴 B）

要求：
- 任意 2 個設備簽名即可轉賬
- 提高安全性
- 適合企業或家庭資金管理

使用工具：
- Electrum
- Specter Desktop
- Trezor Suite（有限支持）
```

#### 3. U2F/FIDO2 認證

```
支持的服務：
- Google
- Facebook
- GitHub
- Dropbox
- 等等...

設置步驟：
1. 進入網站的安全設置
2. 選擇添加安全密鑰
3. 連接 Trezor
4. 按照提示完成註冊
5. 使用 Trezor 進行雙因素認證
```

---

## 開發者指南

### Trezor Connect API

#### JavaScript 集成

```javascript
// 安裝
npm install @trezor/connect-web

// 基本使用
import TrezorConnect from '@trezor/connect-web';

// 初始化
TrezorConnect.init({
    lazyLoad: true,
    manifest: {
        email: 'developer@example.com',
        appUrl: 'https://example.com',
    },
});

// 獲取比特幣地址
const result = await TrezorConnect.getAddress({
    path: "m/49'/0'/0'/0/0",
    coin: 'btc',
});

if (result.success) {
    console.log('地址:', result.payload.address);
} else {
    console.error('錯誤:', result.payload.error);
}
```

#### 簽名交易示例

```javascript
// 比特幣交易簽名
const result = await TrezorConnect.signTransaction({
    inputs: [
        {
            address_n: [44 | 0x80000000, 0 | 0x80000000, 0 | 0x80000000, 0, 0],
            prev_hash: 'b4dc0ffeee...',
            prev_index: 0,
            amount: '100000',
        }
    ],
    outputs: [
        {
            address: '1BitcoinAddress...',
            amount: '90000',
            script_type: 'PAYTOADDRESS',
        },
        {
            address_n: [44 | 0x80000000, 0 | 0x80000000, 0 | 0x80000000, 1, 0],
            amount: '9000',
            script_type: 'PAYTOADDRESS',
        }
    ],
    coin: 'btc',
});
```

#### 以太坊集成

```javascript
// 獲取以太坊地址
const ethAddress = await TrezorConnect.ethereumGetAddress({
    path: "m/44'/60'/0'/0/0",
});

// 簽名以太坊交易
const ethTx = await TrezorConnect.ethereumSignTransaction({
    path: "m/44'/60'/0'/0/0",
    transaction: {
        to: '0x7a250d5630b4cf539739df2c5dacb4c659f2488d',
        value: '0xf4240',
        gasPrice: '0x14',
        gasLimit: '0x14',
        nonce: '0x0',
        chainId: 1,
    },
});

// 簽名消息
const ethMessage = await TrezorConnect.ethereumSignMessage({
    path: "m/44'/60'/0'/0/0",
    message: 'Hello Trezor!',
});
```

### Python 集成

```python
# 安裝
pip install trezor

# 基本使用
from trezorlib import btc, tools
from trezorlib.client import TrezorClient
from trezorlib.transport import get_transport

# 連接設備
transport = get_transport()
client = TrezorClient(transport)

# 獲取地址
address = btc.get_address(
    client,
    "Bitcoin",
    tools.parse_path("m/49'/0'/0'/0/0")
)
print(f"地址: {address}")

# 獲取公鑰
public_key = btc.get_public_node(
    client,
    tools.parse_path("m/49'/0'/0'")
)
print(f"公鑰: {public_key.node.public_key.hex()}")
```

### 自定義幣種集成

```python
# 定義自定義幣種
from trezorlib import coins

custom_coin = {
    'coin_name': 'MyCoin',
    'coin_shortcut': 'MYC',
    'address_type': 48,
    'maxfee_kb': 100000,
    'minfee_kb': 1000,
    'signed_message_header': 'MyCoin Signed Message:\n',
    'xpub_magic': 0x0488b21e,
    'xprv_magic': 0x0488ade4,
    'bip44': 999,
    'segwit': True,
}
```

### 固件開發

#### 構建環境設置

```bash
# 克隆倉庫
git clone https://github.com/trezor/trezor-firmware.git
cd trezor-firmware

# 安裝依賴（Ubuntu/Debian）
sudo apt-get install \
    build-essential git python3 python3-pip \
    libsdl2-dev libsdl2-image-dev gcc-arm-none-eabi \
    libnewlib-arm-none-eabi

# 安裝 Python 依賴
pip3 install poetry
poetry install

# 構建模擬器
cd core
poetry run make build_unix

# 運行模擬器
poetry run ./emu.py
```

#### 固件架構

```
trezor-firmware/
├── core/              # Trezor Model T 固件（Python + C）
│   ├── embed/        # 嵌入式 C 代碼
│   ├── src/          # Python 應用層
│   └── mocks/        # 測試模擬
├── legacy/           # Trezor One 固件（純 C）
│   ├── firmware/     # 主固件
│   └── bootloader/   # 啟動載入程序
├── common/           # 共享資源
│   ├── protob/       # Protocol Buffers 定義
│   └── defs/         # 幣種定義
└── python/           # Python 庫
    └── src/trezorlib/
```

#### 添加新功能示例

```python
# core/src/apps/bitcoin/sign_tx.py

async def sign_tx(ctx, msg):
    """簽名交易的主要入口點"""

    # 驗證輸入
    validate_inputs(msg)

    # 顯示交易詳情給用戶
    await confirm_transaction(ctx, msg)

    # 執行簽名
    signatures = []
    for input in msg.inputs:
        signature = sign_input(input)
        signatures.append(signature)

    return signatures

async def confirm_transaction(ctx, msg):
    """在屏幕上顯示交易供用戶確認"""
    from trezor.ui.layouts import confirm_output

    for output in msg.outputs:
        await confirm_output(
            ctx,
            output.address,
            output.amount,
        )
```

---

## 常見問題

### 安全相關

**Q: 如果我的 Trezor 被盜了怎麼辦？**

A:
1. 不用驚慌 - 沒有 PIN 碼無法訪問
2. 立即購買新 Trezor
3. 使用恢復種子恢復到新設備
4. 將資金轉移到新地址（可選但推薦）

**Q: 忘記 PIN 碼怎麼辦？**

A:
1. 可以使用恢復種子恢復
2. 設備需要清空（wipe）
3. 從種子重新初始化
4. 建議：將 PIN 安全記錄

**Q: Trezor 公司能訪問我的私鑰嗎？**

A: 不能。私鑰是在設備上隨機生成的，永遠不會發送給 Trezor 公司或任何第三方。

**Q: 設備損壞了怎麼辦？**

A:
```
解決方案：
1. 購買新的 Trezor（或兼容的 BIP39 錢包）
2. 使用恢復種子恢復
3. 所有資金將可訪問

預防措施：
- 多個備份副本
- 定期測試恢復流程
- 考慮購買備用設備
```

### 技術問題

**Q: Trezor 支持哪些幣種？**

A:
- Model One: 1000+ 幣種（BTC, ETH, LTC, XRP, ERC20 代幣等）
- Model T: 1450+ 幣種（包括 ADA, XMR, XTZ 等）
- 完整列表：https://trezor.io/coins

**Q: 可以在多台電腦上使用同一個 Trezor 嗎？**

A: 可以。Trezor 可以在任何電腦上使用，私鑰始終保存在設備內。

**Q: Trezor 需要電池嗎？**

A: 不需要。Trezor 通過 USB 供電，沒有內置電池。

**Q: 可以離線使用 Trezor 嗎？**

A:
- 查看地址：需要連接電腦
- 簽名交易：可以離線簽名，然後在另一台在線電腦廣播
- 完全離線（air-gapped）方案需要特殊配置

**Q: 與軟件錢包相比有什麼優勢？**

A:
```
安全性對比：

軟件錢包：
❌ 私鑰存儲在聯網設備
❌ 易受惡意軟件攻擊
❌ 易受鍵盤記錄攻擊

硬件錢包（Trezor）：
✅ 私鑰離線存儲
✅ 物理確認交易
✅ 防惡意軟件
✅ 開源可審計
```

### 使用問題

**Q: 更新固件安全嗎？**

A:
1. 是的，但需要注意：
   - 僅從官方網站下載
   - 驗證簽名
   - 確保有恢復種子備份
2. 固件更新會清空設備（安全特性）
3. 更新後需要從種子恢復

**Q: 如何驗證設備真實性？**

A:
```
驗證步驟：
1. 購買渠道：僅從官方或授權經銷商
2. 包裝檢查：全息防偽標籤
3. 固件檢查：首次啟動會驗證 bootloader
4. 開源驗證：可以自行編譯固件比對

警告標誌：
⚠️ 設備預裝恢復種子
⚠️ 包裝已開封
⚠️ 要求提供恢復種子的郵件
⚠️ 價格過低的二手設備
```

**Q: 交易手續費為什麼有時很高？**

A:
- 手續費由網絡擁堵決定
- Trezor 只是估算，不收取費用
- 可以自定義手續費
- 使用 SegWit 地址可降低費用

---

## 最佳實踐總結

### 安全檢查清單

```
✅ 初始化
□ 從官方渠道購買
□ 檢查包裝密封
□ 在設備上生成種子（不使用預裝）
□ 離線記錄恢復種子
□ 驗證恢復種子
□ 設置強 PIN 碼（8+ 位）

✅ 日常使用
□ 始終在設備屏幕上驗證地址
□ 小額測試交易
□ 定期更新固件
□ 使用官方 Trezor Suite
□ 啟用密碼短語（高價值賬戶）

✅ 備份
□ 多份恢復種子副本（3+）
□ 不同地點存放
□ 考慮金屬備份
□ 永不電子存儲或拍照
□ 定期測試恢復流程

✅ 高級安全
□ 使用隱藏錢包（密碼短語）
□ 考慮多簽名設置
□ 定期審計資金
□ 使用專用電腦（高價值操作）
```

### 常見錯誤避免

```
❌ 永遠不要做：
1. 分享恢復種子
2. 在聯網設備上輸入恢復種子
3. 拍照或截圖恢復種子
4. 購買二手 Trezor
5. 使用簡單的 PIN（如 1234）
6. 忽略設備屏幕上的警告
7. 在釣魚網站輸入信息
8. 跳過小額測試交易

✅ 始終要做：
1. 驗證接收地址
2. 檢查交易詳情
3. 保持固件更新
4. 安全存儲備份
5. 使用官方軟件
6. 小額測試後再大額轉賬
```

---

## 資源鏈接

### 官方資源
- 官網：https://trezor.io
- 文檔：https://wiki.trezor.io
- 支持：https://trezor.io/support
- 博客：https://blog.trezor.io
- GitHub：https://github.com/trezor

### 開發資源
- API 文檔：https://docs.trezor.io/trezor-firmware
- Connect API：https://github.com/trezor/connect
- Python 庫：https://github.com/trezor/trezor-firmware/tree/master/python

### 社區
- Reddit：r/TREZOR
- Twitter：@Trezor
- Forum：https://forum.trezor.io

### 學習資源
- BIP39 詳解：https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
- BIP32 詳解：https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
- BIP44 詳解：https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki

---

## 總結

Trezor 硬件錢包代表了加密貨幣安全存儲的黃金標準。通過以下特點確保資產安全：

### 核心優勢
1. **離線存儲**：私鑰永不接觸網絡
2. **開源透明**：代碼可審計，無後門
3. **用戶控制**：完全掌控私鑰和資產
4. **多層保護**：PIN、密碼短語、物理確認
5. **恢復機制**：助記詞確保資產可恢復

### 適用人群
- 長期持有者（HODLers）
- 大額資產持有者
- 注重安全的用戶
- 加密貨幣企業
- 開發者和技術愛好者

### 關鍵要點
```
記住：
"Not your keys, not your coins"
（不是你的私鑰，就不是你的幣）

Trezor 讓您真正擁有加密貨幣的所有權。
```

### 下一步行動
1. 訪問官網了解更多信息
2. 選擇適合的型號（One 或 T）
3. 從官方渠道購買
4. 仔細完成初始化設置
5. 安全存儲恢復種子
6. 開始安全地管理數字資產

---

**免責聲明**：本教學僅供教育目的。加密貨幣投資存在風險，請根據自身情況謹慎決策。始終從官方渠道獲取最新信息。

**版本**：v1.0
**最後更新**：2025-11
**作者**：Trezor 技術教學項目組
