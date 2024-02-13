from functools import reduce
from operator import mul

class Packet:
    def __init__(self):
        self.version = ''
        self.type = ''
        self.literal = ''
        self.num_bits = 0
        self.subpackets = []

    def set_packet_len(self):
        self.num_bits = 6
        if self.type == '100':
            self.num_bits += len(self.literal)
            self.num_bits += len(self.literal) // 4
        else:
            self.num_bits += 1
            self.num_bits += 15 if self.length_type_id == '0' else 11
        for subpacket in self.subpackets:
            self.num_bits += subpacket.num_bits

def hex_to_bin(hex_num):
    bin_num = hex_num

    for i in range(16):
        hex_char = str(hex(i))[2:].upper()
        bin_repr = str(bin(i))[2:].zfill(4)
        bin_num = bin_num.replace(hex_char, bin_repr)

    return bin_num

def parse_packet(packet_str):
    packet = Packet()
    packet.version = packet_str[0:3]
    packet.type = packet_str[3:6]

    if int(packet.type, 2) == 4:
        # literal value
        i = 6
        while True:
            packet.literal += packet_str[i+1: i+5]
            if packet_str[i] == '0': break
            i += 5

    else:
        # operator
        packet.length_type_id = packet_str[6]
        packet.length_type_num = packet_str[7:7+15] if packet.length_type_id == '0' else packet_str[7:7+11]
        
        if packet.length_type_id == '0':
            # length of subpackets
            i = 0
            while i < int(packet.length_type_num, 2):
                # add new subpacket, increment length counter by subpacket length
                packet.subpackets.append(parse_packet(packet_str[22+i:]))
                i += packet.subpackets[-1].num_bits
        
        else:
            # number of subpackets
            i = 18
            for _ in range(int(packet.length_type_num, 2)):
                # add new subpacket, increment index counter by subpacket length
                packet.subpackets.append(parse_packet(packet_str[i:]))
                i += packet.subpackets[-1].num_bits
            
    packet.set_packet_len()
    return packet

def version_sum(packet):
    v_sum = int(packet.version, 2)
    for subpacket in packet.subpackets:
        v_sum += version_sum(subpacket)
    return v_sum

def eval_packet(packet):
    packet_type = int(packet.type, 2)
    sub_vals = [eval_packet(x) for x in packet.subpackets]

    if   packet_type == 0: return sum(sub_vals)
    elif packet_type == 1: return reduce(mul, sub_vals, 1)
    elif packet_type == 2: return min(sub_vals)
    elif packet_type == 3: return max(sub_vals)
    elif packet_type == 4: return int(packet.literal, 2)
    elif packet_type == 5: return 1 if sub_vals[0] > sub_vals[1] else 0
    elif packet_type == 6: return 1 if sub_vals[0] < sub_vals[1] else 0
    elif packet_type == 7: return 1 if sub_vals[0] == sub_vals[1] else 0
    
def day16_part1(input):
    bin_str = hex_to_bin(input)
    packet = parse_packet(bin_str)
    return version_sum(packet)

def day16_part2(input):
    bin_str = hex_to_bin(input)
    packet = parse_packet(bin_str)
    return eval_packet(packet)

if __name__ == "__main__":
    test_input = open('input.txt', 'r').read()

    assert day16_part1('D2FE28') == 6
    assert day16_part1('38006F45291200') == 9
    assert day16_part1('EE00D40C823060') == 14
    assert day16_part1('8A004A801A8002F478') == 16
    assert day16_part1('620080001611562C8802118E34') == 12
    assert day16_part1('C0015000016115A2E0802F182340') == 23
    assert day16_part1('A0016C880162017C3686B18A3D4780') == 31
    print(day16_part1(test_input))

    assert day16_part2('C200B40A82') == 3
    assert day16_part2('04005AC33890') == 54
    assert day16_part2('880086C3E88112') == 7
    assert day16_part2('CE00C43D881120') == 9
    assert day16_part2('D8005AC2A8F0') == 1
    assert day16_part2('F600BC2D8F') == 0
    assert day16_part2('9C005AC2F8F0') == 0
    assert day16_part2('9C0141080250320F1802104A08') == 1
    print(day16_part2(test_input))