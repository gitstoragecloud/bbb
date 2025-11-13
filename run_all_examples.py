"""
運行所有量子電路範例
"""

import sys
import time


def print_header(title):
    """打印美化的標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def run_example(example_name, example_module):
    """運行單個範例"""
    print_header(f"運行範例：{example_name}")

    start_time = time.time()

    try:
        # 動態匯入模組
        __import__(example_module)
        elapsed_time = time.time() - start_time

        print(f"\n✓ {example_name} 執行成功！")
        print(f"  耗時: {elapsed_time:.2f} 秒")

        return True

    except Exception as e:
        elapsed_time = time.time() - start_time

        print(f"\n✗ {example_name} 執行失敗！")
        print(f"  錯誤: {str(e)}")
        print(f"  耗時: {elapsed_time:.2f} 秒")

        return False


def main():
    """主程式"""
    print_header("Qiskit 量子電路範例集 - 全部執行")

    print("準備運行所有範例...\n")
    print("注意：這可能需要幾分鐘時間\n")

    # 定義所有範例
    examples = [
        ("範例 1：基本量子閘操作", "example_01_basic_gates"),
        ("範例 2：量子糾纏", "example_02_entanglement"),
        ("範例 3：量子疊加與干涉", "example_03_superposition_interference"),
        ("範例 4：量子演算法", "example_04_quantum_algorithms"),
        ("範例 5：實際應用", "example_05_practical_applications"),
    ]

    # 運行統計
    results = []
    start_time = time.time()

    # 運行每個範例
    for name, module in examples:
        success = run_example(name, module)
        results.append((name, success))
        time.sleep(1)  # 短暫暫停

    # 總結
    total_time = time.time() - start_time

    print_header("執行總結")

    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print(f"總共執行: {total_count} 個範例")
    print(f"成功: {success_count} 個")
    print(f"失敗: {total_count - success_count} 個")
    print(f"總耗時: {total_time:.2f} 秒")

    print("\n詳細結果:")
    for name, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")

    # 輸出文件列表
    print("\n生成的結果文件:")
    result_files = [
        "example_01_results.txt",
        "example_02_results.txt",
        "example_03_results.txt",
        "example_04_results.txt",
        "example_05_results.txt",
    ]

    for f in result_files:
        print(f"  - {f}")

    print("\n" + "=" * 70)
    print("  所有範例執行完畢！")
    print("=" * 70)

    # 如果有失敗，返回非零退出碼
    if success_count < total_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
