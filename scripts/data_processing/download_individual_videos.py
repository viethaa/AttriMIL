#!/usr/bin/env python3
"""
Download individual video files from Google Drive.

This script downloads videos one-by-one instead of as a folder,
which is more reliable and avoids Google Drive's folder zipping issues.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


# File IDs from the Google Drive folder
# Format: (file_id, filename, class)
ADENOMA_FILES = [
    ("1iCaAK43oy9yCzNfgqZHNaOpoZt7zvr74", "1.avi", "Adenoma"),
    ("1Va8_jiEIsUR-oGIIkk_VRy2Zgh8FoyJF", "2.avi", "Adenoma"),
    ("1BK3I3oWUdns8Z_RW0YBRwpQmt6hNgPvw", "3.avi", "Adenoma"),
    ("1fSJEBzXTMw1PjEzt_7qhL05FlXT3CJDL", "4.avi", "Adenoma"),
    ("15szx_vYY7tQP-aau7zziJSJj1ofSCLVx", "5.avi", "Adenoma"),
    ("1541GI1AsjxV-XULJ7CvvM0umQIlPsO0X", "21b8981.avi", "Adenoma"),
    ("11poVHzWbf02_LA8qCaAng5oCJwJ6Iolv", "24a0125.avi", "Adenoma"),
    ("1fVRp-d1FZojfAsWSck-75WY3AafTZgGV", "24a0140.avi", "Adenoma"),
    ("1rfzKeskAj0e-RGXG08iqu2xjELtfd4Kr", "24a0141.avi", "Adenoma"),
    ("11qPeih9910TeWv2mGUmzebWeN6L-IWgt", "24a0350.avi", "Adenoma"),
    ("1G4oXenLuEe0SWP5ubhq4G4eIfyCPItDu", "24a0633.avi", "Adenoma"),
    ("1CAHt5cMBz562XBqTsZB648a04niO7oUb", "24a0705.avi", "Adenoma"),
    ("1rvYayHdk-vTMMUGilmrxAxcwlEC8tf5I", "24a0763.avi", "Adenoma"),
    ("1hlARH12mm6krrKC07yw_dNRE2r2aOQMK", "24a0986.avi", "Adenoma"),
    ("1Y4pury68e0pEK_Rkh_HPXisbHD6Gm3iR", "24a0987.avi", "Adenoma"),
    ("1pdMpM-5IFB-MrlSZr0fbUQUA2hvcPYXf", "24a1140.avi", "Adenoma"),
    ("1TCeHERcOBW5eHCNJ5wjFNuHEwnAnCvr4", "24a1522.avi", "Adenoma"),
    ("1Op5KhQSd2LoRPZQFHgYTEwDg53A7ff0j", "24a1676.avi", "Adenoma"),
    ("1Ldi_VfdXE4CKnAMGkZpD9Q5DCrK__3wq", "24a1680.avi", "Adenoma"),
    ("1O1_P-bWZNvzzPguJUVvt7nmQLZrIsG-I", "24a1814.avi", "Adenoma"),
    ("1_lqmDP5psSzHINTDyU0Ik8_pwXHBxf4r", "24a2096.avi", "Adenoma"),
    ("1WT8JGQ9C9R9QDDtuNJRZzf_rXYbClI-z", "24a2232.avi", "Adenoma"),
    ("1_FRdtbZ-9vQhv1sboSsNWjqFSBBVQHEm", "24a2386.avi", "Adenoma"),
    ("1n32hrHzFXQbBpJVS-X_ezBdB0-vJoZ9d", "24a2782.avi", "Adenoma"),
    ("1iwaWVM0igKFxJxAvHskKQGKgmbqZxkFd", "24a2784.avi", "Adenoma"),
    ("1S_FCyQgrxfPH6qPaoYiKmmmfUJ3sAPfZ", "24a2900.avi", "Adenoma"),
    ("1QIE8f86CVWUQTS2305A-4WrRXIjXzos3", "24a3261.avi", "Adenoma"),
    ("1JiUzJsdUF5taIpjtOSzc3tfwtspYTTbv", "24a3415.avi", "Adenoma"),
    ("1Bhs_ShDeJ9s0K6GQ5xE5KAcOB--1SU7k", "24a4121.avi", "Adenoma"),
    ("1sb83XB0ouO6JMwkuu2jsi-0ctZ6Ov6Oz", "24a4127.avi", "Adenoma"),
    ("1Ec5cpfgch19vf7bicpeDYKNmRHGvCU4L", "24a4415.avi", "Adenoma"),
    ("1IC2oKEa4sgxk80ZjM0_QeW3ms-G6241t", "24a4554.avi", "Adenoma"),
    ("1KKwmn_xtLPtD8KdYHq6NMbDZ1_58U66N", "24a5614.avi", "Adenoma"),
    ("1EsEaQRzVm57Ursit5kIGRA32_QmTjPH1", "24a5759.avi", "Adenoma"),
    ("122LlhnnQ-J0D1BK4ikCBYK1YVmoqH237", "24a5913.avi", "Adenoma"),
    ("1yvDO0dPEEtpVAHLBuKNe68ZhIHQfE2iT", "24a6155.avi", "Adenoma"),
    ("1PaFfLtoReYDdS0YAkFhe884tqx2IYbPg", "24a6428.avi", "Adenoma"),
    ("1fM9S-PLHy2mMO7-_cDPfA113ByqxNYkk", "24a6433.avi", "Adenoma"),
    ("1zd3FLqOV5kGXVAIgP2GRE1JyGPAhNHYw", "24a6435.avi", "Adenoma"),
    ("1KiXYKwbDDzbG21AqKXGCsv8sC_E-42JH", "24a6713.avi", "Adenoma"),
    ("1IxVKCHVoHKoCGGjRvPqoxhsEIAAJdIhe", "24a6937.avi", "Adenoma"),
    ("1ytir-KyLkuPC3FS6eQHJhfyP4odOrNh7", "24a6941.avi", "Adenoma"),
    ("10rBK8_cp3HYCaPT5zLwlOegI2TJ6wieC", "24a7166.avi", "Adenoma"),
    ("1TeVoMSSiSLFsZdnxITonWhvoBuca0mxi", "24a7276.avi", "Adenoma"),
    ("1V4SR_3k3sOAZKwC0mUVhKd2d88LWzwGT", "24a7387.avi", "Adenoma"),
    ("1GE4M8yNYIvrHcL8L0PHWnVfkYJQKCmAQ", "24a7580.avi", "Adenoma"),
    ("1y9vlAy0CBJ96uGWsGbO4L2hT0zL3WUQI", "24a7729.avi", "Adenoma"),
    ("1RyJ4oGvdjF9w62a5rlCnpreiyR39F6TT", "24a7814.avi", "Adenoma"),
    ("1oZkwvi2CbKjeC4j9AaJMg1TAwai700kt", "24a8419.avi", "Adenoma"),
    ("1oJtLlJ0fQVGNvmb_BBe-iJsLlo5GnTkQ", "24a8737.avi", "Adenoma"),
]

MALIGNANT_FILES = [
    ("1zu5_Sd2lclH_PE9FE_6JM5Hg2u_hmNwT", "10.avi", "Malignant"),
    ("17gKExbf6LCbAkl94I8ciWHUf7azpGwcK", "11.avi", "Malignant"),
    ("1PF9pTqigtpWGMPWGd6ElCIvS5zpZvXtf", "12.avi", "Malignant"),
    ("1f_Y5ufyfciA0ZNCYFDwbbLHZgCcStMe7", "13.avi", "Malignant"),
    ("1NuhINj2gUbiFfiMJfsdcicHKKWUFPWSX", "24a0271.avi", "Malignant"),
    ("1guITll53urO8uN5q5CkneU5Ip-euAN7d", "24a0496.avi", "Malignant"),
    ("119bq1ocnd7guzLlWcGyGZQp4mS3yjDdZ", "24a0497.avi", "Malignant"),
    ("1ZElX_dbyeRb_QHd3WKw3HoGqNCUajN0U", "24a785.avi", "Malignant"),
    ("1ihy_C5lOvhN8DMd5xBMzojChvOyDOyvS", "24a1386.avi", "Malignant"),
    ("1oA5Uq4KNKM5uEoiUVMJQgt1x9EWzHohy", "24a1393.avi", "Malignant"),
    ("1VyEx4rT_6dZsb8ZhhlZvxXD9tevwr5bb", "24a1826.avi", "Malignant"),
    ("105Ck0g_vnWEZewbHXlMu9LN4uDGHIBeR", "24a2083.avi", "Malignant"),
    ("1UgTZUT4uFvnw4Rl7UaLEukRQvzCgOp9-", "24a2086.avi", "Malignant"),
    ("1vOHG4Hw_lxJ1RLDN7K_QFOxo34BoPUTw", "24a2206.avi", "Malignant"),
    ("1ySLAgO8dUO00kBWGbbkP6MltbZJ_erga", "24a2658.avi", "Malignant"),
    ("1nCqZMawroJZLYPOCFnY3mpbD9lJN-AOS", "24a2998.avi", "Malignant"),
    ("1J5yXaHqVZeCyQMqYrklBH22DDL-sMnNI", "24a3358.avi", "Malignant"),
    ("1bqg2IlhTZ95OwK4s-5x2PMtDrwBw0c0A", "24a3360.avi", "Malignant"),
    ("1Y8GsoN0yEf03VMkiK_OEaEDv83b8iCtv", "24a3993.avi", "Malignant"),
    ("1ozO1H7W_oOwSC6TxWiXFFaI0I0Odn7TG", "24a4273.avi", "Malignant"),
    ("1SUTGps-WI-SGOEGbjC5vDvTUw4QMkvja", "24a4393.avi", "Malignant"),
    ("1Y5D0P3e8UU4OfFAmHGCx41llYXya_Zeu", "24a5136.avi", "Malignant"),
    ("1X7VS7YITgiDuv8Rmt3gDVcynXxTyF2CI", "24a5320.avi", "Malignant"),
    ("1xq5UnPHe5us1_2PBVrX8PbnXuHyX-gOo", "24a5377.avi", "Malignant"),
    ("10xJVL5C3qRyol9G8CW4KvWNpHzVph3DR", "24a6287.avi", "Malignant"),
    ("1R-dWGbnvrFITvcvp7zSv1cYf-GawFmmh", "24a6411.avi", "Malignant"),
    ("1519iWcSlloM3Rvx9mBPi7eE-3DpIJ2zB", "24a6432.avi", "Malignant"),
    ("1oqGIBXhVMAvliOf9mXQY3abzu6uGrPa9", "24a6962.avi", "Malignant"),
    ("1kxTAS16DYLvd6k4CHX3fSYxLOO3M9Q7N", "24a7097.avi", "Malignant"),
    ("1AHZXxrGDPK0TcFb_DYcHm9IAxXefSFz7", "24a7165.avi", "Malignant"),
    ("1HGe-19R0jQ3RGHNhd4ltSxdtgRDghISV", "24a7392.avi", "Malignant"),
    ("1C3xTN_GMxfej-f_G3EIMyu8ARQTmLzvn", "24a7401.avi", "Malignant"),
    ("1hN6ZBOmLzt8pKPw8PCETQLoDFx9f48bl", "24a7572.avi", "Malignant"),
    ("16npiEuqJ14WiO_6cKHzl7zDdPm8kr3NJ", "24a7972.avi", "Malignant"),
    ("1x4y29jnaL40Pq_S__PK1U-xjNm0I1b32", "24a8261.avi", "Malignant"),
    ("1Guv2a9Ezu0wFuPKEFobtNIcsc8xhsXQq", "24a8744.avi", "Malignant"),
    ("1vn5ypx3-wNA9G_fJ9iCMekVLOJ_mVYjT", "24a9256.avi", "Malignant"),
    ("1EsFadxAS-ek09fIM_v4FB9_wzaMC2Uu_", "24a9817.avi", "Malignant"),
    ("1YOISexDdaV02eHH8zvwe5DVgBQjhjDJ5", "24a9941.avi", "Malignant"),
    ("1zOxplb3UeQo0-sE88-wO57CAiSPkW1So", "24a9942.avi", "Malignant"),
    ("1XHCPlQxQ1WB_04GCNVR5NkgGsG0X4Bzw", "24b0359.avi", "Malignant"),
    ("1-OGQoJjvBDg8YUYTf-p9BW7Nu6_rGkie", "24b0468.avi", "Malignant"),
    ("15fck4Cr8UbRNhe35-oXp_s4NDM_bx99m", "24b0641.avi", "Malignant"),
    ("16vTigrofIHgF_8MCiOw-k1CwmgjPcXI9", "24b1026.avi", "Malignant"),
    ("1gOoPo0Db93exYl1F85W-7UL0CE5Gvaey", "24b1027.avi", "Malignant"),
    ("13d-_GiFzifDXhyMOjDuC5AY77-0VlMn7", "24b1028.avi", "Malignant"),
    ("17oEGdKg31TR7-H11eA1N-vDt7bI9jHTX", "24b1031.avi", "Malignant"),
    ("1lvK7YjhINUXxEIGyYdSTvrdWbh90L6i4", "24b1038.avi", "Malignant"),
    ("18iXi4qpOEV7HAsp2hUYWwdXo6V7Zt6dy", "24b1039.avi", "Malignant"),
    ("174u9O6PwTXp03SG8pffu58TYtPBVIV4i", "24b1354.avi", "Malignant"),
]

NORMAL_FILES = [
    ("1tBHFUEDphtCM57dMkSwzv4EiJ9kk8zxE", "24a0631.avi", "Normal"),
    ("1OnM0Ij52gp9JVeTpSBEdetKj52cb8qz6", "24a0791.avi", "Normal"),
    ("1Pecn8CJFuXFAHslnJWLGP3xokuV3sKPK", "24a1536.avi", "Normal"),
    ("1D8M91EGCLoZBv8GuaElhod-zejdHqe7L", "24a1673.avi", "Normal"),
    ("1145tuy104bVE10P2uCTXOJsPEzGUy68P", "24a1684.avi", "Normal"),
    ("1l-Oausq5Ks8HKjjNI2QahgqIsasMhN1m", "24a1813.avi", "Normal"),
    ("1JFKK0NiGTEJgdugAOgPPIkTUQJkjq9OM", "24a1820.avi", "Normal"),
    ("1dQmrAdU_BdmKxMz0UE-JSPtJZ9hq3hCt", "24a1829.avi", "Normal"),
    ("1ohbohMp0WTPLtrBSPvFkSa6oZeJeqvfw", "24a1837.avi", "Normal"),
    ("1YBiTx8yRcAltjH-rmRJtftP6u5qxsSCi", "24a1967.avi", "Normal"),
    ("1GzUrP8HsyJMujsn3pcLVheP264MVdndA", "24a2079.avi", "Normal"),
    ("1T6u8ojirOJCFsKvyZ2hy0oDPEGRxxq--", "24a2902.avi", "Normal"),
    ("1SaBZxCGBYuL_Hc1xBb8gvu8A_TlhI57b", "24a4129.avi", "Normal"),
    ("1MUG8Zn1wKoavFwGRbRqinmbaeV1labhc", "24a4564.avi", "Normal"),
    ("1VJiOZjbQLXPAogdNI-OmirHuNStv8XKM", "24a4714.avi", "Normal"),
    ("1AgXcnCAY08G9pxG0Hlw1MVRjFgcqoZ4u", "24a5265.avi", "Normal"),
    ("1qAs9GifSGbMQyQQ90Uba9jyRNWwHWHd-", "24a5322.avi", "Normal"),
    ("14xeLtVf53_VDbx3FLkhbRbEPXx5zDrVt", "24a5909.avi", "Normal"),
    ("1aT0oboQ2XGy1ryWBsZ5OKSviwEhCTWH8", "24a6110.avi", "Normal"),
    ("1Jlbf_w7a2xuQs2zxa14sYFt11L4PgAPh", "24a6426.avi", "Normal"),
    ("1QJumsymNeUZzhRbdljjcFP0YrbDF9MmW", "24a6434.avi", "Normal"),
    ("1uT_GTcFWctphMBiF5aHH5F9xAX1B0IBi", "24a6762.avi", "Normal"),
    ("18nK172lyQ6j28-zUkDZcVK8NUSYg7UMa", "24a6938.avi", "Normal"),
    ("1Ocy7vUhfgcCzdeKwLyV8Iu_MZSvhWTZn", "24a7770.avi", "Normal"),
    ("1YgGrspV-4RJUgxOFOp7fDV3n9DxOx-KA", "24a8119.avi", "Normal"),
    ("1-Xb0skD4OuNl0OChTvVQlVKo3CG4V_7y", "24a8821.avi", "Normal"),
    ("17p2KnQa0XvhkB1flGzdTFKX5hsChjIr6", "24a8823.avi", "Normal"),
    ("1BVQXjgaxfZydGOcQqkcSSNnbsr3hEXI2", "24a9529.avi", "Normal"),
    ("1OLuzMSLZUBbTsDFrrmKlDUSUB6CfAlkY", "24a9622.avi", "Normal"),
    ("1wk5OGfAnQyaqI1CAa77-fNO2WHk_PojN", "24a9816.avi", "Normal"),
    ("1-tAF-2UsEGDflWmg5y0RukdH3wg6te5i", "24b0146.avi", "Normal"),
    ("1ejsvG9ijSZfUkteZXglNIG2xdXyS7VdQ", "24b0309.avi", "Normal"),
    ("1A3U3HmRldYFcRVopvWih4S8sIx6syuyN", "24b0368.avi", "Normal"),
    ("1itcjS3f0Ol_195INNFF-YBBtN_JLnMoj", "24b0649.avi", "Normal"),
    ("1FoazvG0YiJfH1-vOZphRxjGmFHf1MVrY", "24b0830.avi", "Normal"),
    ("1HZqpj3tqitXTVvNqVAoRzJ4346D3hBuB", "24b0879.avi", "Normal"),
    ("1bu5_qZRc0C_RTlJYsAwjw1X9rlVvNTLS", "24b1327.avi", "Normal"),
    ("11UrWqWvUvDVTNk3YndXLN6Ipn2YipMkK", "24b2161.avi", "Normal"),
    ("1KDjUsz2GDpB6SoghtNUHptSEE4jstnuS", "24b2365.avi", "Normal"),
    ("1_ZBTM6Tu4_MkqzPY7Msz35IvYEHAXfwo", "24b2522.avi", "Normal"),
    ("1jVa7zWLbn0TT6XsRWSYvuHu3ansmBLxr", "24b2657.avi", "Normal"),
    ("12KPcgOwUUUJkQBRX5hYlMDh9jg6l49MK", "24b2971.avi", "Normal"),
    ("1TKbCEROK_0dfPj3iJlfL5009nPh1bBii", "24b4048.avi", "Normal"),
    ("1ioIEV5UH_ze7it8qehWAZUtJmENBc6Hk", "24b8292.avi", "Normal"),
    ("1MLL-ltrcBxCtYmJCMdiFLQ9lG9QvWmNI", "24b9110.avi", "Normal"),
    ("1eCYAJg1ITUe7L31mr7ATi2_RFeOR-jl5", "24d6252.avi", "Normal"),
    ("1x5UHYU_-jGuJWDt1jKAp3RqIvvl1FSKm", "24d6272.avi", "Normal"),
    ("13YJr_dXRnZ8Dybd5qbWLcjnpLMtGRkyr", "24d6276.avi", "Normal"),
    ("1OB_7pQDnfnAue38mk_Njt51PXcizOsYo", "24d6369.avi", "Normal"),
]

ALL_FILES = ADENOMA_FILES + MALIGNANT_FILES + NORMAL_FILES


def download_file(file_id, output_path, max_retries=3):
    """Download a single file from Google Drive."""
    for attempt in range(max_retries):
        try:
            cmd = ["gdown", f"https://drive.google.com/uc?id={file_id}", "-O", str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                return True, None
            else:
                error = result.stderr if result.stderr else result.stdout
                if "too many users" in error.lower() or "rate limit" in error.lower():
                    return False, "rate_limit"
                return False, error
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"    Timeout, retrying ({attempt + 2}/{max_retries})...")
                continue
            return False, "timeout"
        except Exception as e:
            return False, str(e)

    return False, "max_retries_exceeded"


def main():
    parser = argparse.ArgumentParser(description="Download individual videos from Google Drive")
    parser.add_argument("--output-dir", type=str, default="data/full_dataset",
                       help="Output directory (default: data/full_dataset)")
    parser.add_argument("--class", dest="class_filter", type=str, choices=["Adenoma", "Malignant", "Normal"],
                       help="Only download files from specific class")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                       help="Skip files that already exist (default: True)")
    parser.add_argument("--delay", type=float, default=2.0,
                       help="Delay between downloads in seconds (default: 2.0)")

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    # Filter files by class if specified
    if args.class_filter:
        files_to_download = [f for f in ALL_FILES if f[2] == args.class_filter]
    else:
        files_to_download = ALL_FILES

    print(f"Total files to download: {len(files_to_download)}")
    print(f"Output directory: {output_dir.absolute()}")
    print()

    # Track statistics
    downloaded = 0
    skipped = 0
    failed = 0
    rate_limited = 0

    for i, (file_id, filename, class_name) in enumerate(files_to_download, 1):
        class_dir = output_dir / class_name
        class_dir.mkdir(parents=True, exist_ok=True)

        output_path = class_dir / filename

        # Skip if exists
        if args.skip_existing and output_path.exists():
            print(f"[{i}/{len(files_to_download)}] SKIP {class_name}/{filename} (already exists)")
            skipped += 1
            continue

        print(f"[{i}/{len(files_to_download)}] Downloading {class_name}/{filename}...", end=" ", flush=True)

        success, error = download_file(file_id, output_path)

        if success:
            print("✓")
            downloaded += 1
        elif error == "rate_limit":
            print("✗ RATE LIMITED")
            rate_limited += 1
            print(f"\n⚠️  Hit rate limit after {downloaded} downloads.")
            print("Wait 30-60 minutes and run again with --skip-existing to continue.\n")
            break
        else:
            print(f"✗ Failed: {error}")
            failed += 1

        # Delay between downloads
        if i < len(files_to_download):
            time.sleep(args.delay)

    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Downloaded:    {downloaded}")
    print(f"Skipped:       {skipped}")
    print(f"Failed:        {failed}")
    print(f"Rate Limited:  {rate_limited}")
    print(f"Total:         {len(files_to_download)}")
    print("="*60)

    # Count current videos
    print("\nCurrent video count:")
    for class_name in ["Adenoma", "Malignant", "Normal"]:
        class_dir = output_dir / class_name
        if class_dir.exists():
            count = len(list(class_dir.glob("*.avi")))
            print(f"  {class_name:12s}: {count}")

    return 0 if rate_limited == 0 and failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
