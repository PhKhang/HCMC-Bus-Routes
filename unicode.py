import unicodedata

print("THẠNH LỘC" == "THẠNH LỘC")

a = "THẠNH LỘC"
b = "THẠNH LỘC"
print(len(a))
print(len(b))
print(unicodedata.normalize("NFC", "THẠNH LỘC")  == unicodedata.normalize("NFC", "THẠNH LỘC") )

# print("Ộ" == "Ộ")
# for i in range(len("THẠNH LỘC") + 1):
#     print(ord(a[i]), end=' ')
#     print(ord(b[i]))
#     print(a[i])
