class BaseSharingScheme:
    def __init__(self, num_shares, threshold):
        assert threshold > 0 and threshold < num_shares, 'Threshold out of range'

        self.num_shares = num_shares
        self.threshold = threshold

    def share(self, secret):
        raise NotImplementedError

    def recombine(self, shares):
        raise NotImplementedError

    def verify_shares(self, shares):
        raise NotImplementedError