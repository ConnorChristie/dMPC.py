from mpc.sharing.base import BaseSharingScheme

import mpc.utils.polynomials as poly_utils

class ShamirSharingScheme(BaseSharingScheme):
    def share(self, secret):
        polynomial = poly_utils.generate_random_polynomial_by_intercept(self.threshold, secret.field, secret)

        share_ids = [x for x in range(1, self.num_shares + 1)]
        shares = poly_utils.evaluate_polynomial(polynomial, share_ids, secret.field)

        return shares

    def recombine(self, shares):
        assert len(shares) > self.threshold, 'Not enough shares to compute secret'
        return self._recombine(shares)

    @staticmethod
    def _recombine(shares, eval_point=0):
        return poly_utils.lagrange_interpolation(eval_point, shares)

    def verify_shares(self, shares):
        return poly_utils.verify_polynomial(shares, self.threshold)

    def reshare(self, share, new_ids):
        polys = []

        share_id = share[0]
        share_val = share[1]

        for new_id in new_ids:
            V = poly_utils.generate_random_polynomial_by_intercept(self.threshold, share_val.field, 0, 1234)
            V_y = poly_utils.evaluate_polynomial(V, [share_id], share_val.field)[0][1]

            Wk = poly_utils.generate_random_polynomial_by_root(self.threshold, share_val.field, new_id, 1234)
            Wk_y = poly_utils.evaluate_polynomial(Wk, [share_id], share_val.field)[0][1]

            polys.append((new_id, V_y + Wk_y))

        return [(x[0], share_val + x[1]) for x in polys]
