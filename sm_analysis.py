import random
import re

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

# 素数判定
def is_prime(q):
    q = abs(q)
    if q == 2:
        return True
    if q < 2 or q & 1 == 0:
        return False
    return pow(2, q-1, q) == 1

#
# 関数：decimal_to_binary_len
# 引数：10進数整数n
# 機能：10進数nを2進数に直し，その桁数を返す．
# 返り値：2進数の桁数
#
def decimal_to_binary_len(n):
    return len(bin(n)[2:])

# 鍵長がkey_lengthの素数をランダムに生成する．
def random_prime_number(key_length):
  while True:
    tmp = random_integer(2**(key_length-1), 2**(key_length)-1)
    if is_prime(tmp):
      return tmp

def ex_euclid(x, y):
  c0, c1 = x, y
  a0, a1 = 1, 0
  b0, b1 = 0, 1

  while c1 != 0:
    m = c0 % c1
    q = c0 // c1

    c0, c1 = c1, m
    a0, a1 = a1, (a0 - q * a1)
    b0, b1 = b1, (b0 - q * b1)

  return c0, a0, b0

# rsaの鍵を設定する．
def rsa_setting(p_length, q_length, e):
  p = random_prime_number(p_length)
  q = random_prime_number(q_length)
  n = p*q

  _, a, _ = ex_euclid(e, (p-1)*(q-1))
  d = a % ((p-1)*(q-1))
  dp = d % (p-1)
  dq = d % (q-1)

  if (e*d % ((p-1)*(q-1)) == 1):
    return p, q, d, dp, dq, n
  else:
    return -1,-1,-1,-1,-1,-1

# step1: sm→1
def step1(sm):
  for i in range(len(sm)-1):
    if sm[i:i+2] == 'sm':
      sm = sm[:i] + '1' + sm[i+2:]
  return sm

# step2: ここの0を別の文字で置き換えて，extension_step3で利用する！
def step2(sm, w):
  flag = True
  while flag:
    flag = False
    for i in range(0, w-1):
      my_regex = "1[^1]{" + str(i) + "}1[^1]{" + str(w-1-i) + "}"
      result = re.finditer(my_regex, sm)
      for m in result:
        index = m.span()[1]
        before_sm = sm
        sm = sm[:index-(w-1-i)] + '0'*(w-1-i) + sm[index:]
        if before_sm != sm:
          flag = True
  return sm

# extension_step3
def extension_step3(sm, w):
  flag = True
  while flag:
    flag = False
    for i in range(0, w-1):
      my_regex = "[^1]{" + str(w-1-i) + "}10{" + str(i) + "}[z1]"
      result = re.finditer(my_regex, sm)
      for m in result:
        print(m)
        index = m.span()[0]
        before_sm = sm
        sm = sm[:index] + 'z' + sm[index+1:]
        if before_sm != sm:
          flag = True
  return sm

# step3: 
def step3(sm, w):
  flag = True
  while flag:
    flag = False
    my_regex = "[^1]{" + str(w-1) + "}11"
    result = re.finditer(my_regex, sm)
    for m in result:
      index = m.span()[0]
      before_sm = sm
      sm = sm[:index] + 'z' + sm[index+1:]
      if before_sm != sm:
        flag = True
  return sm

# step4:
def step4(sm, w):
  flag = True
  while flag:
    flag = False
    i = 0
    while i <= (len(sm)-1):
      if sm[i] == '1':
        j = i+1
        while j <= (len(sm)-1) and sm[j] != '1':
          j += 1
        if (j-i-1) >= w:
          sm = sm[:i+1] + '0'*(j-i-w) + sm[j-w+1:]
        i = j
      else:
        i += 1

  return sm

if __name__ == '__main__':
  window_length = 4
  e = 2**16+1

  # p, q, d, dp, dqの計算
  p, q, d, dp, dq, n = rsa_setting(32, 32, e)
  p_list = change_decimal_to_binary(p)
  q_list = change_decimal_to_binary(q)
  d_list = change_decimal_to_binary(d)
  dp_list = change_decimal_to_binary(dp)
  dq_list = change_decimal_to_binary(dq)
  
  # k, kp, kqの計算
  if ((e*d-1)%((p-1)*(q-1)) == 0):
    k = (e*d-1) // ((p-1)*(q-1))
  else:
    print('k is error')

  if ((e*dp-1) % (p-1) == 0):
    kp = (e*dp-1) // (p-1)
  else:
    print('kp is error')

  if ((e*dq-1) % (q-1) == 0):
    kq = (e*dq-1) // (q-1)
  else:
    print('kq is error')

  # dp, dqのSM時系列導出
  dp_sm = change_d_to_sm_series(dp_list, window_length)
  dq_sm = change_d_to_sm_series(dq_list, window_length)

  dp_sm = "s1sssssss1sss1ssss1sss1ss1ssss11sssss1ssssss1s1sssss1ss1sssssss1"
  dq_sm = "s1sssssss1sss1ssss1sss1ss1ssss11sssss1ssssss1s1sssss1ss1sssssss1"
  dp_sm = "sssmssssssmsssmsssssmsmssssssmssssssm"
  dq_sm = "sssmssssssmsssmsssssmsmssssssmssssssm"

  print(dp_sm)
  print(dq_sm)

  before_dp_sm = dp_sm
  before_dq_sm = dq_sm

  # step1: sm → 1
  print('*** step1 ***')
  dp_sm = step1(dp_sm)
  dq_sm = step1(dq_sm)
  print(dp_sm)
  print(dq_sm)

  # step2: 
  print('*** step2 ***')
  dp_sm = step2(dp_sm, window_length)
  dq_sm = step2(dq_sm, window_length)
  print(dp_sm)
  print(dq_sm)

  # extension step2:
  print('*** extension step2 ***')
  dp_sm = extension_step3(dp_sm, window_length)
  dq_sm = extension_step3(dq_sm, window_length)
  print(dp_sm)
  print(dq_sm)

  # step3:
  print('*** step3 ***')
  dp_sm = step3(dp_sm, window_length)
  dq_sm = step3(dq_sm, window_length)
  print(dp_sm)
  print(dq_sm)

  # step4:
  print('*** step4 ***')
  dp_sm = step4(dp_sm, window_length)
  dq_sm = step4(dq_sm, window_length)
  print(dp_sm)
  print(dq_sm)

  while before_dp_sm != dp_sm or before_dq_sm != dq_sm:
    before_dp_sm = dp_sm
    before_dq_sm = dq_sm

    # step1: sm → 1
    print('*** step1 ***')
    dp_sm = step1(dp_sm)
    dq_sm = step1(dq_sm)
    print(dp_sm)
    print(dq_sm)

    # step2:
    print('*** step2 ***')
    dp_sm = step2(dp_sm, window_length)
    dq_sm = step2(dq_sm, window_length)
    print(dp_sm)
    print(dq_sm)

    # extension step2:
    print('*** extension step2 ***')
    dp_sm = extension_step3(dp_sm, window_length)
    dq_sm = extension_step3(dq_sm, window_length)
    print(dp_sm)
    print(dq_sm)

    # step3:
    print('*** step3 ***')
    dp_sm = step3(dp_sm, window_length)
    dq_sm = step3(dq_sm, window_length)
    print(dp_sm)
    print(dq_sm)

    # step4:
    print('*** step4 ***')
    dp_sm = step4(dp_sm, window_length)
    dq_sm = step4(dq_sm, window_length)
    print(dp_sm)
    print(dq_sm)
