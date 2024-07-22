# app/utils.py
import time
import threading

class SnowflakeIDGenerator:
    def __init__(self, node_id: int, epoch: int = 1288834974657):
        self.node_id = node_id
        self.epoch = epoch
        self.node_id_bits = 10
        self.sequence_bits = 12
        self.max_node_id = -1 ^ (-1 << self.node_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

        if node_id > self.max_node_id or node_id < 0:
            raise ValueError(f"Node ID must be between 0 and {self.max_node_id}")

        self.node_id_shift = self.sequence_bits
        self.timestamp_left_shift = self.sequence_bits + self.node_id_bits
        self.sequence_mask = self.max_sequence

        self.last_timestamp = -1
        self.sequence = 0
        self.lock = threading.Lock()

    def _timestamp(self):
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp):
        timestamp = self._timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._timestamp()
        return timestamp

    def generate_id(self):
        with self.lock:
            timestamp = self._timestamp()

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards. Refusing to generate id")

            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp
            return ((timestamp - self.epoch) << self.timestamp_left_shift) | (self.node_id << self.node_id_shift) | self.sequence

# 实例化 Snowflake ID 生成器
snowflake_id_generator = SnowflakeIDGenerator(node_id=1)
