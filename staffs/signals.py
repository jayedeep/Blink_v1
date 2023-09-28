from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from staffs.models import OrderPrepare, Ledger, LedgerLine


@receiver(post_save, sender=OrderPrepare)
def create_ledger_for_order(sender, instance, created, **kwargs):
    create_ledger = Ledger(ledger_type='order',order_id_id=instance.order_id.id)
    create_ledger.save()
    if instance.order_id.payment_set.last.payment_method == 'Online':
        for orderline in instance.order_id.order.all():
            LedgerLine.objects.create(ledger_id=create_ledger.id, orderline_id=orderline.id, type_of_transaction='credit',
                                      amount=orderline.sub_total_amount,
                                      description=f'Transaction Credited for Order ID:{orderline.order_id.orderid} for Product {orderline.product_id}')
        if instance.order_id.vouchers:
            discount_amount = sum([i.sub_total_amount for i in instance.order_id.order.all()]) - instance.order_id.amount

            if discount_amount:
                LedgerLine.objects.create(ledger_id=create_ledger.id,
                                          type_of_transaction='debit',
                                          amount=discount_amount,
                                          description=f'Transaction Debited for Order ID:{instance.order_id.orderid} for Voucher Discount {instance.order_id.vouchers}')

