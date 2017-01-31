from datetime import datetime

from django.db import models


#Managers
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from base.signals import proposal_accepted, changing_event_data, changing_item_data
from stripe_cater.models import PaymentOrder


class EventManager(models.Manager):
    ERROR = -1
    ERRORS = [ERROR]
    def get_event_by(self, id):
        return self.get(pk=id)

    def create_or_update_invoice_from_event(self, data, invoice, handly = False):

        if invoice:
            response = self.create_or_update_proposal_from_event(data, proposal=invoice.proposal)
            if response in self.ERRORS:
                return response
            else:
                invoice.update_due_date(data.get('due_date'))
                changing_event_data.send(sender=Invoice,invoice=invoice)
                return invoice
        else:
           response = self.create_or_update_proposal_from_event(data, from_invoice= handly)
           if response in self.ERRORS:
                return response
           else:
                response = Invoice.objects.create_from_proposal(due_date=data.get('due_date'),proposal=response)
                if response in Invoice.objects.ERRORS:
                    return self.ERROR
                else:
                    return response

    def create_or_update_proposal_from_event(self, data, proposal=None, from_invoice=False):
        comment = data.get('comment')
        if proposal:
            response = self.create_or_update_event(data=data, instance=proposal.event)
            if response not in self.ERRORS:
                proposal.client_message = comment
                proposal.save()
                changing_event_data.send(sender=Proposal,proposal=proposal)
                return proposal
            else:
                return response
        else:
            response = self.create_or_update_event(data=data )
            if response in self.ERRORS:
                return response


            try:
               proposal =  Proposal.objects.create_proposal(event=response,client_message=comment, from_invoice=from_invoice)
               return proposal
            except Exception as e:
                print(e)
                return self.ERROR


    def create_or_update_event(self, data, instance=None):
        name = data.get('name')
        address = data.get('address')
        event_date = data.get('event_date')
        # due_date = data.get('due_date')
        customer = data.get('customer')

        try:
            if instance:
                instance.name = name
                instance.address = address
                instance.event_date = event_date
                # instance.due_date = due_date
                instance.customer = customer

                instance.save()

                return instance
            else:
                event = self.create(name=name, address=address, event_date = event_date,
                                    # due_date=due_date,
                                    customer=customer)

                return event
        except Exception as e:
            print(e)
            return self.ERROR

class ProposalManager(models.Manager):
    ERROR = -1
    ERROR_TOKEN = -2
    ERROR_EXPIRED = -3
    ERROR_INVOICE = -4
    ERROR_PRESUPUESTO_ACCEPTADO =-5
    ERROR_PRESUPUESTO_DENEGADO= -6
    OK = 0
    ERRORS = [ERROR, ERROR_TOKEN,ERROR_EXPIRED]
    def generate_number(self):
        return int(datetime.today().timestamp() * 1000000)
    def create_proposal(self, event, client_message, from_invoice=False):
        status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.EDITTING)
        if from_invoice:
            status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
        return self.create(event=event, status=status, number=self.generate_number(), client_message=client_message)

    def get_by_id(self, id, business=None, hide_cancelled=True):
        query = self.filter(id=id)
        if hide_cancelled:
          query = query.exclude(status=N_Proposal_Status.CANCELLED)
        if business:
            query = query.filter(event__customer__business=business)
        p = query.first()
        if p:
            return p
        else:
            return self.ERROR

    def get_by_business(self, business, hide_cancelled=True):
        query = self.filter(event__customer__business=business)
        if hide_cancelled:
           query =  query.exclude(status=N_Proposal_Status.CANCELLED)
        return query



    def deny_proposal(self, id, token):
        p = self.filter(id=id).filter(send_token=token).filter(status=N_Proposal_Status.PENDING).first()
        if p:
            if p.has_expired():
                return self.ERROR_EXPIRED
            p.deny()
            # p.reset_token()
            # p.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.DENIED)
            # p.save()
            return p
        else:
            return self.ERROR_TOKEN

    def accpet_proposal(self, id, token):
        p = self.filter(id=id).filter(send_token=token).filter(status=N_Proposal_Status.PENDING).first()
        if p:
            if p.has_expired():
                return self.ERROR_EXPIRED
            response = p.accept()

            if response in Invoice.objects.ERRORS:
                return self.ERROR_INVOICE
            # p.reset_token()
            # p.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
            # p.save()
            return p
        else:
            return self.ERROR_TOKEN

    def cancell_proposal(self, proposal):
        try:
            proposal.status = N_Proposal_Status.objects.get(id=N_Proposal_Status.CANCELLED)
            proposal.save()
            return self.OK
        except:
            return self.ERROR



class InvoiceManager(models.Manager):
    ERROR = -1
    ERROR_TOKEN = -2
    ERROR_EXPIRED = -3
    OK = 0
    ERRORS = [ERROR, ERROR_EXPIRED, ERROR_TOKEN]
    def generate_number(self):
        return str(int(datetime.today().timestamp() * 1000000))

    def create_from_proposal(self, proposal, handly = True, due_date=None):
        try:
            # status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.CREATED)
            # if handly:
            status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.EDITTING)

            due_date_value = proposal.event.event_date
            if due_date:
                due_date_value = due_date

            invoice = self.create(due_date=due_date_value,
                number=self.generate_number(), proposal=proposal, status=status)
            return invoice
        except Exception as e:
            print(e)
            return self.ERROR

    def get_by_id(self, id, business=None, hide_deleted=True):
        query = self.filter(id=id)
        if hide_deleted:
          query = query.exclude(deleted=True)
        if business:
            query = query.filter(proposal__event__customer__business=business)
        inv = query.first()
        if inv:
            return inv
        else:
            return self.ERROR

    def get_invoice_to_pay_by_id(self, id, token):
        invoice = self.filter(id=id).filter(send_token=token).first()

        if invoice and invoice.status.id == N_Invoice_Status.PENDING:
            return invoice
        else:
            return self.ERROR


    def get_by_business(self, business, hide_deleted=True):
        query = self.filter(proposal__event__customer__business=business)
        if hide_deleted:
           query = query.exclude(deleted=True)
        return query



    def delete_invoice(self, invoice):
        response = Proposal.objects.cancell_proposal(invoice.proposal)
        if response in Proposal.ERRORS:
            return self.ERROR
        try:
            invoice.deleted = True
            invoice.save()
            return self.OK
        except:
            return self.ERROR

    def get_invoice_by_payment(self, payment):
        return self.filter(payment_order=payment).first()

    def get_by_proposal(self, proposal):
        return self.filter(proposal=proposal).first()

    def chekc_due_date(self, business=None):
        today = datetime.today()
        query = Invoice.objects.filter(status=N_Invoice_Status.PENDING).filter(due_date__lt=today)
        if business:
            query = query.filter(proposal__event__customer__business=business)
        query.update(status=N_Invoice_Status.PAST_DUE)

class ItemManager(models.Manager):
     ERROR = -1
     ERRORS = [ERROR]
     def update_item(self, data, item):
          try:
              oferta = data.get('oferta')
              oferta = Oferta.objects.get_oferta_by_name(name=oferta, business=item.oferta.business)
              discount = data.get('discount')
              unit_cost = data.get('unit_cost')
              quantity = data.get('quantity')
              tax = data.get('tax') or item.proposal.get_tax()
              description = data.get('description')

              item.tax = tax
              item.oferta = oferta
              item.discount = discount
              item.description = description
              item.unit_cost = unit_cost
              item.quantity = quantity

              item.save()
              changing_item_data.send(sender=None, proposal=item.proposal)
              return item
          except:
              return self.ERROR

     def delete_item(self,id):
         try:
            item = self.get(pk=id)
            changing_item_data.send(sender=None, proposal=item.proposal)
            item.delete()
         except Exception as e:
             print(e)
             pass



#Models
from base.models import Customer, Oferta


class Event(models.Model):
    objects = EventManager()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    # due_date = models.DateField()
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return self.name

class Request(models.Model):
    event = models.ForeignKey(Event)
    oferta = models.ForeignKey(Oferta)
    quantity = models.IntegerField()




class Proposal(models.Model):

    DEFAULT_TOKEN_VALUE = '0'
    ERROR = -1
    ERRORS = [ERROR]
    objects = ProposalManager()
    event = models.ForeignKey(Event)
    status = models.ForeignKey('N_Proposal_Status')
    client_message = models.TextField(max_length=150, null=True, default='')
    number = models.CharField(default='0', max_length=50)
    send_token = models.CharField(default=DEFAULT_TOKEN_VALUE, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    denied_by_system = models.BooleanField(default=False)

    def get_items(self):
        return self.item_set.all()

    def __str__(self):
        return self.event.name

    def get_item_by_id(self, id):
        try:
            return self.item_set.get(pk=id)
        except:
            return self.ERROR

    def add_item(self, data, business):
        try:
            oferta = data.get('oferta')
            oferta = Oferta.objects.get_oferta_by_name(name=oferta, business=business)
            discount = data.get('discount')
            unit_cost = data.get('unit_cost')
            quantity = data.get('quantity')
            tax = data.get('tax') or self.get_tax()
            description = data.get('description')

            item = Item.objects.create(tax=tax, quantity=quantity,oferta=oferta, discount=discount, description=description, unit_cost=unit_cost, proposal=self)
            changing_item_data.send(sender=None, proposal=self)
            return item
        except Exception as e:
            print(e)
            return self.ERROR

    def get_total(self):
        return sum([item.grant_total() for item in self.get_items()])

    # def get_subtotal(self):
        return sum([item.sub_total() for item in self.get_items()])

    def get_subtotal(self):
        return sum([item.total() for item in self.get_items()])

    def get_taxes(self):
        return sum([item.sub_total()*item.tax for item in self.get_items()])/100

    def get_total_discount(self):
        return sum([item.total() - item.grant_total() for item in self.get_items()])

    def get_tax(self):
        return self.event.customer.business.tax / 100

    def may_send_email(self):
        return self.status.id in [N_Proposal_Status.DENIED, N_Proposal_Status.EDITTING, N_Proposal_Status.PENDING]

    def may_be_editted(self):
        return self.status.id not in [N_Proposal_Status.ACCEPTED, N_Proposal_Status.CANCELLED]


    def has_expired(self):
        return self.event.event_date.date() < datetime.date(datetime.today())

    def generate_token(self):
        if self.send_token == Proposal.DEFAULT_TOKEN_VALUE:
            token = int(datetime.today().timestamp() * 1000000)
            self.send_token = str(token)
            self.save()
            token = urlsafe_base64_encode(force_bytes(token))
        else:
            token = urlsafe_base64_encode(force_bytes(int(self.send_token)))
        return token

    def deny_by_business(self):
        if self.status.id == N_Proposal_Status.PENDING:
            self.deny(system=True)
            return self
        return self.ERROR

    def accept_by_business(self):
        if self.status.id in [N_Proposal_Status.PENDING, N_Proposal_Status.DENIED]:
            self.accept()
            return self
        return self.ERROR

    def deny(self, system=False):
        self.reset_token()
        self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.DENIED)
        self.denied_by_system = system
        self.save()

    def accept(self):
          response = Invoice.objects.create_from_proposal(proposal=self, handly=False)
          if response in Invoice.objects.ERRORS:
               return response
          self.reset_token()
          self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.ACCEPTED)
          self.save()
          proposal_accepted.send(sender=Proposal, proposal=self)

    def reset_token(self):

        self.send_token = Proposal.DEFAULT_TOKEN_VALUE
        self.save()

    def has_been_sent(self):
        self.status = N_Proposal_Status.objects.get(pk=N_Proposal_Status.PENDING)
        self.save()



class Invoice(models.Model):

    DEFAULT_TOKEN_VALUE = '0'
    objects = InvoiceManager()
    proposal = models.ForeignKey(Proposal)
    status = models.ForeignKey('N_Invoice_Status')
    # order = models.ForeignKey(Order, null=True)
    number = models.CharField(default='0', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    send_token = models.CharField(default=DEFAULT_TOKEN_VALUE, max_length=50)
    payment_order = models.ForeignKey(PaymentOrder, null=True)
    deleted = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.now())

    def update_due_date(self, due_date):
        self.due_date = due_date
        self.save()

    def __str__(self):
        return self.proposal.event.name

    def generate_token(self):
        token = int(datetime.today().timestamp() * 1000000)
        self.send_token = str(token)
        self.save()
        token = urlsafe_base64_encode(force_bytes(token))
        return token

    def has_been_sent(self):
        self.status = N_Invoice_Status.objects.get(pk=N_Invoice_Status.PENDING)
        self.save()

    def reset_token(self):
        self.send_token = Invoice.DEFAULT_TOKEN_VALUE
        self.save()

    def may_send_email(self):
        return self.status.id in [N_Invoice_Status.EDITTING, N_Invoice_Status.PENDING]

    def check_status(self):
        if self.payment_order.has_been_paid():
            self.status = N_Invoice_Status.objects.get(id=N_Invoice_Status.PAID)
            self.save()

    def set_payment(self, payment):
        self.payment_order = payment
        self.save()

    def has_payment_order(self):
        return self.payment_order != None

class Item(models.Model):
    objects = ItemManager()
    proposal = models.ForeignKey(Proposal)
    oferta = models.ForeignKey(Oferta)
    tax = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.oferta.name

    def sub_total(self):
        return self.quantity * self.unit_cost

    def total(self):
        sub_total = self.sub_total()
        return sub_total*( 1 + self.tax/100)

    def grant_total(self):
        value = self.total()
        return value - value * self.discount / 100



#Nomenclators

class N_Proposal_Status(models.Model):
    EDITTING = 1
    PENDING = 2
    ACCEPTED = 3
    DENIED = 4
    CANCELLED = 5
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'

class N_Invoice_Status(models.Model):
    # CREATED = 1
    EDITTING = 2
    PENDING = 3
    PAID = 4
    PAST_DUE = 5
    # CANCELLED = 5
    # ACCEPTED = 6
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'base'
