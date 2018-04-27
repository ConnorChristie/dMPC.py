from mpc.sharing import (
    BaseSharingScheme,
    ShamirSharingScheme,
)

from mpc.field import (
    GF64,
)

from hashlib import sha1

import random as rand
import hmac

class PseudoRandomSecretShare(BaseSharingScheme):
    def __init__(self, shareholder_ids, *args, **kwargs):
        BaseSharingScheme.__init__(self, *args, **kwargs)
        self.shareholder_ids = shareholder_ids

    def generate_seeds(self, shareholders, field):
        max_unqualified_set = self._generate_subsets(shareholders, self.num_shares - self.threshold, field)
        return [(subset, self._generate_key()) for subset in max_unqualified_set]

    def share(self, id, prfs, key):
        """
        Return a pseudo-random secret share for a random number.

        The share is for player *j* based on the pseudo-random functions
        given in *prfs* (a mapping from subsets of players to :class:`PRF`
        instances). The *key* is used when evaluating the PRFs.

        share_p1_q1 = prf_p1_q1(key=1)
        share_p1_q2 = prf_p1_q2(key=1)

        peer[0].prf = PRF()
        """

        replicated_shares = self.random_replicated_sharing(id, prfs, key)
        return self.replicated_to_shamir(id, replicated_shares)

    def zero_share(self, id, prfs, key, quantity=1):
        """Return *quantity* pseudo-random secret zero-sharings of degree 2t.
        """
        # We start by generating t random numbers for each subset. This is
        # very similar to calling random_replicated_sharing t times, but
        # by doing it like this we immediatedly get the nesting we want.
        rep_shares = [(s, [(i + 1, prf((key, i))) for i in range(self.threshold)])
                    for (s, prf) in prfs.iteritems() if id in s]

        print(rep_shares)

        # We then proceed with the zero-sharing. The first part is like in
        # a normal PRSS.
        result = [id.field(0)] * quantity

        for subset, shares in rep_shares:
            points = [(x, id.field(0)) for x in self.shareholder_ids - subset] + [(id.field(0), id.field(1))]
            f_in_j = ShamirSharingScheme._recombine(points, eval_point=id)

            # Unlike a normal PRSS we have an inner sum where we use a
            # degree 2t polynomial g_i which we choose as
            #
            #   g_i(x) = f(x) * x**j
            #
            # since we already have the degree t polynomial f at hand. The
            # g_i are all linearly independent as required by the protocol
            # and can thus be used for the zero-sharing.
            for i, packed_share in shares:
                g_i_in_j = f_in_j * id**i

                for k in range(quantity):
                    result[k] += packed_share * g_i_in_j

        return result[0]

    def replicated_to_shamir(self, id, replicated_shares):
        """
        Convert a set of replicated shares to a Shamir share.

        The conversion is done for player *j* (out of *n*) and will be
        done over *field*.
        """
        result = id.field(0)

        for subset, share in replicated_shares:
            points = [(x, share.field(0)) for x in self.shareholder_ids - subset] + [(share.field(0), share.field(1))]
            f_in_j = ShamirSharingScheme._recombine(points, eval_point=id)
            result += share * f_in_j

        return result

    @staticmethod
    def random_replicated_sharing(id, prfs, key):
        """
        Return a replicated sharing of a random number.

        The shares are for player *j* based on the pseudo-random functions
        given in *prfs* (a mapping from subsets of players to :class:`PRF`
        instances). The *key* is used when evaluating the PRFs. The result
        is a list of ``(subset, share)`` pairs.
        """
        # The PRFs contain the subsets we need, plus some extra in the
        # case of dealer_keys. That is why we have to check that j is in
        # the subset before using it.
        return [(s, prf(key)) for (s, prf) in prfs.iteritems() if id in s]

    @staticmethod
    def _generate_subsets(orig_set, size, field):
        """
        Generates the set of all subsets of a specific size.
        """

        if len(orig_set) > size:
            result = set()

            for element in orig_set:
                result.update(PseudoRandomSecretShare._generate_subsets(orig_set - set([element]), size, field))

            return frozenset(result)
        elif len(orig_set) == size:
            return frozenset([orig_set])
        else:
            return frozenset()

    @staticmethod
    def _generate_key():
        # TODO: is a 40 byte hex string as good as a 20 byte binary
        # string when it is used for SHA1 hashing? It ought to be
        # since they contain the same entropy.

        # A SHA1 hash is 160 bit
        return hex(rand.randint(0, 2 ** 160))

class PRF(object):
    """
    Models a pseudo random function (a PRF).
    """

    def __init__(self, key, field):
        """
        Create a PRF keyed with the given key and max.
        """
        self.key = key
        self.field = field

    def __call__(self, input):
        """
        Return a number based on input.
        """
        hasher = hmac.new(self.key, str(hash(input)), sha1)
        return self.field(int(hasher.hexdigest(), 16))
