import random

# a以上b以下の数値をランダムに生成する．
def random_integer(a, b):
  return random.randint(a, b)

# 引数a(10進数)を2進数に変換する．
def change_decimal_to_binary(a):
  return [int(i) for i in list(bin(a)[2:])]

# 秘密鍵配列d_listをsm時系列に変換する(ウィンドウ幅w)．
def change_d_to_sm_series(d_list, w):
  resolve_d_list = []
  i = 0
  len_d = len(d_list)
  while i < len_d:
    if d_list[i] == 0:
      resolve_d_list.append([0])
      i += 1
    else:
      if i+w < len_d:
        l = w
      else:
        l = (len_d - i)

      tmp_list = d_list[i:i+l]
      # 右端0を削除
      for j in range(i+l-1, i-1, -1):
        if d_list[j] == 1:
          break
      resolve_d_list.append(tmp_list[0:(j-i+1)])
      i += (j-i+1)

  sm = ""
  for block in resolve_d_list:
    if block == [0]:
      sm += "s"
    else:
      for _ in range(len(block)):
        sm += "s"
      sm += "m"

  # print('ブロックの分割結果(w = {1}): {0}'.format(resolve_d_list, w))
  return sm

if __name__ == '__main__':
  d = random_integer(2**4000, 2**4001)
  d_list = change_decimal_to_binary(d)

  print(change_d_to_sm_series(d_list, 4))
