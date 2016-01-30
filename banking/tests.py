from django.test import TestCase

from .models import Event, User, Transaction, Transfer


class UserBalanceTest(TestCase):
    def setUp(self):
        User.objects.create(username="P1", rate=1)
        a = User.objects.create(username="Author", rate=0)
        Event.objects.create(name="test", price=1000, author=a)

    def test_transfer_sould_up_balance(self):
        p1 = User.objects.get(username="P1")

        Transfer.objects.create(user=p1, debit=100)
        Transfer.objects.create(user=p1, debit=300)
        Transfer.objects.create(user=p1, debit=400)

        self.assertEqual(p1.balance(), 800)

    def test_transactions_change_balance(self):
        """ When user have transfers and transactions."""
        p1 = User.objects.get(username="P1")
        e = Event.objects.get(name="test")
        #########################################
        Transfer.objects.create(user=p1, debit=100)
        Transfer.objects.create(user=p1, debit=300)
        Transfer.objects.create(user=p1, debit=400)
        Transaction.objects.create(user=p1, event=e, credit=200)
        Transaction.objects.create(user=p1, event=e, debit=300)
        #########################################
        self.assertEqual(p1.balance(), 900)


class EventParticipationTest(TestCase):
    ubalance = 3000
    eprice = 3000
    u1_r = 1
    u2_r = 1
    u3_r = 1
    u4_r = 1
    u5_r = 0.5
    u6_r = 0.5
    u1_p = 1
    u2_p = 2
    u3_p = 3
    u4_p = 4
    u5_p = 1
    u6_p = 1.5

    def setUp(self):
        a = User.objects.create(username="Author")
        Event.objects.create(name="Target", price=self.eprice, author=a)

        p1 = User.objects.create(username="P1", rate=self.u1_r)
        p2 = User.objects.create(username="P2", rate=self.u2_r)
        p3 = User.objects.create(username="P3", rate=self.u3_r)
        p4 = User.objects.create(username="P4", rate=self.u4_r)
        p5 = User.objects.create(username="P5", rate=self.u5_r)
        p6 = User.objects.create(username="P6", rate=self.u6_r)
        users = [p1, p2, p3, p4, p5, p6]

        for u in users:
            Transfer.objects.create(user=u, debit=self.ubalance)

    def test_single_participation(self):
        """ When user participate in event(1part)."""
        e = Event.objects.get(name="Target")
        u = User.objects.get(username="P1")

        print("Run test_single_participation")
        #########################################
        e.add_participants({u: 1})
        #########################################

        self.assertEqual(u.balance(), 0)
        self.assertEqual(e.rest(), 0)
        print("END test_single_participation")

    def test_multiple_participation(self):
        """ When user participate in event, where someone already participated.
        Should create Transactions for each participant on each new
        participation. Should increace balance of already participated user."""

        e = Event.objects.get(name="Target")
        users = User.objects.filter(username__iregex=r'^P\d$')
        #########################################
        e.add_participants({
            users[0]: 1,
            users[1]: 1,
            users[2]: 1,
            users[3]: 1
        })

        #########################################
        self.assertEqual(len(Transaction.objects.filter(user=users[0])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[1])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[2])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[3])), 1)

        party_pay = self.eprice / (len(users) - 2)

        self.assertEqual(users[0].balance(),
                         self.ubalance - party_pay * self.u1_r)
        self.assertEqual(users[1].balance(),
                         self.ubalance - party_pay * self.u2_r)
        self.assertEqual(users[2].balance(),
                         self.ubalance - party_pay * self.u3_r)
        self.assertEqual(users[3].balance(),
                         self.ubalance - party_pay * self.u4_r)

    def test_multiple_participation_with_different_parts(self):
        """ When calculating debt with participation-parts value."""
        e = Event.objects.get(name="Target")
        users = User.objects.filter(username__iregex=r'^P\d$')
        participation = {
            users[0]: self.u1_p,
            users[1]: self.u2_p,
            users[2]: self.u3_p,
            users[3]: self.u4_p
        }

        print("RUN test_multiple_participation_with_different_parts")
        #########################################
        e.add_participants(participation)
        #########################################

        self.assertEqual(len(Transaction.objects.filter(user=users[0])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[1])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[2])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[3])), 1)

        print(Transaction.objects.all())
        party_pay =\
            self.eprice / (self.u1_p * self.u1_r + self.u2_p * self.u2_r
                           + self.u3_p * self.u3_r + self.u4_p * self.u4_r)

        self.assertEqual(e.rest(), 0)

        self.assertEqual(users[0].balance(),
                         self.ubalance - party_pay * self.u1_p * self.u1_r)
        self.assertEqual(users[1].balance(),
                         self.ubalance - party_pay * self.u2_p * self.u2_r)
        self.assertEqual(users[2].balance(),
                         self.ubalance - party_pay * self.u3_p * self.u3_r)
        self.assertEqual(users[3].balance(),
                         self.ubalance - party_pay * self.u4_p * self.u4_r)
        print("END test_multiple_participation_with_different_parts")

    def test_diff_parts_rates(self):
        """ Different parts counts, and user rates."""
        e = Event.objects.get(name="Target")
        users = User.objects.filter(username__iregex=r'^P\d$')
        participation = {
            users[0]: self.u1_p,
            users[1]: self.u2_p,
            users[4]: self.u5_p,
            users[5]: self.u6_p
        }

        print("RUN test_multiple_participation_with_different_parts")
        #########################################
        e.add_participants(participation)
        #########################################

        self.assertEqual(len(Transaction.objects.filter(user=users[0])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[1])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[4])), 1)
        self.assertEqual(len(Transaction.objects.filter(user=users[5])), 1)

        print(Transaction.objects.all())
        party_pay =\
            self.eprice / (self.u1_p * self.u1_r + self.u2_p * self.u2_r
                           + self.u5_p * self.u5_r + self.u6_p * self.u6_r)

        self.assertEqual(e.rest(), 0)

        self.assertEqual(users[0].balance(),
                         self.ubalance - party_pay * self.u1_p * self.u1_r)
        self.assertEqual(users[1].balance(),
                         self.ubalance - party_pay * self.u2_p * self.u2_r)
        self.assertEqual(users[4].balance(),
                         self.ubalance - party_pay * self.u5_p * self.u5_r)
        self.assertEqual(users[5].balance(),
                         self.ubalance - party_pay * self.u6_p * self.u6_r)
        print("END test_multiple_participation_with_different_parts")
