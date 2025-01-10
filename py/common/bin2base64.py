import base64, sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        bin_file = sys.argv[1]
        with open(bin_file, "rb") as f:
            binary_data = f.read()
            text_data = base64.b64encode(binary_data).decode('utf-8')
            print("Base64 txt:", text_data)
            f.close()
    elif len(sys.argv) == 3:
        binary_data = base64.b64decode(sys.argv[1])
        bin_file = sys.argv[2]
        with open(bin_file, "wb") as f:
            f.write(binary_data)
            f.close()
        print("Base64 save to:", bin_file)
    else:
        print("binary to base64-text: python3 <file-from>")
        print("base64-text to binary: python3 \"<base64 text>\" <file-to>")