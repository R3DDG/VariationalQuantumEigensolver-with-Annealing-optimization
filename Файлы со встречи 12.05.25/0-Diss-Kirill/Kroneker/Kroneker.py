import numpy as np
s0 = [[1,0],[0,1]] 
s1 = [[0,1], [1,0]]
s2 = [[0,-1j], [1j,0]]
s3 = [[1,0],[0,-1]]
s3000 = np.kron( s3, np.kron( s0, np.kron(s0,s0) ) )
s0300 = np.kron( s0, np.kron( s3, np.kron(s0,s0) ) )
#
s0030 = np.kron( s0, np.kron( s0, np.kron(s3,s0) ) )
s0003 = np.kron( s0, np.kron( s0, np.kron(s0,s3) ) )
#
s3300 = np.kron( s3, np.kron( s3, np.kron(s0,s0) ) )
#
s3030 = np.kron( s3, np.kron( s0, np.kron(s3,s0) ) )
s0303 = np.kron( s0, np.kron( s3, np.kron(s0,s3) ) )
#
s3003 = np.kron( s3, np.kron( s0, np.kron(s0,s3) ) )
s0330 = np.kron( s0, np.kron( s3, np.kron(s3,s0) ) )
#
s0033 = np.kron( s0, np.kron( s0, np.kron(s3,s3) ) )
#
s2112 = np.kron( s2, np.kron( s1, np.kron(s1,s2) ) )
s2211 = np.kron( s2, np.kron( s2, np.kron(s1,s1) ) )
s1122 = np.kron( s1, np.kron( s1, np.kron(s2,s2) ) )
s1221 = np.kron( s1, np.kron( s2, np.kron(s2,s1) ) )
H = 0.178*(s3000+s0300) - 0.243*(s0030+s0003) + 0.171*s3300 \
+ 0.123*(s3030+s0303) + 0.168*(s3003+s0330) + 0.176*s0033 \
+ 0.045*(s2112-s2211-s1122+s1221)
#
#open('H.txt', mode='w', encoding="utf-8")
Hr = H.real
with open("matrixH.txt", "w") as f:
    f.write('\n'.join([''.join(map(str, line)) for line in Hr]))
np.savetxt('matH.txt', Hr, delimiter=',')
print(Hr)