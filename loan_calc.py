import argparse
import math

parser = argparse.ArgumentParser(description="This program lets you calculate a couple loan related things.")

parser.add_argument("--type", choices=["annuity", "diff"], required=True, help="Choose between annuity and differentiated payment.")
parser.add_argument("--payment", help="Specify a payment amount per period for annuity payment.")
parser.add_argument("--principal", help="Specify a principal amount of the loan.")
parser.add_argument("--periods", help="Specify the number of months you loan the money for.")
parser.add_argument("--interest", help="Specify the interest percentage.")

args = parser.parse_args()


def nominal_interest(interest):
    return interest / (12 * 100)


def overpay(principal, total_pay):
    return math.ceil(total_pay - principal)


def annuity_payment(interest, months, principal):
    nominal = nominal_interest(interest)
    result = math.ceil(principal * (
        (nominal * math.pow((1 + nominal), months)) / (math.pow((1 + nominal), months) - 1)))
    total_payment = result * months
    print(f'Your monthly payment = {result}!')
    print(f'Overpayment = {overpay(principal, total_payment)}')


def differentiate_payment(interest, periods, principal):
    nominal = nominal_interest(interest)
    total_payment = 0
    for i in range(1, periods+1):
        payment = math.ceil((principal / periods) + nominal * (principal - ((principal * (i - 1)) / periods)))
        print(f'Month {i}: payment is {payment}')
        total_payment += payment
    print(f'Overpayment = {overpay(principal, total_payment)}')


def number_of_payments(annuity, interest, principal):
    nominal = nominal_interest(interest)
    result = math.ceil(math.log((annuity / (annuity - (nominal * principal))), (1 + nominal)))
    total_payment = annuity * result
    years = result // 12
    months = result % 12
    if years == 0:
        if result == 1:
            print('It will take 1 month to repay this loan!')
        else:
            print(f'It will take {months} months to repay this loan!')
    elif months == 0:
        if years == 1:
            print('It will take 1 year to repay this loan!')
        else:
            print(f'It will take {years} years to repay this loan!')
    else:
        print(f'It will take {years} years and {months} months to repay this loan!')
    print(f'Overpayment = {overpay(principal, total_payment)}')


def principal_loan(annuity, interest, months):
    nominal = nominal_interest(interest)
    total_payment = annuity * months
    result = annuity / (
        (nominal * math.pow((1 + nominal), months)) / (math.pow((1 + nominal), months) - 1))
    print(f'Your loan principal = {result}!')
    print(f'Overpayment = {overpay(result, total_payment)}')


choices = [args.type, args.payment, args.principal, args.periods, args.interest]
choices_filter = list(filter(None, choices))
choices_numbers = choices_filter[1:]


def main():
    if len(choices_filter) < 4 or any(float(i) < 0 for i in choices_numbers):
        print('Incorrect parameters')
    elif args.type == 'annuity':
        if args.interest and args.periods and args.principal:
            annuity_payment(float(args.interest), int(args.periods), int(args.principal))
        elif args.payment and args.interest and args.periods:
            principal_loan(int(args.payment), float(args.interest), int(args.periods))
        elif args.payment and args.interest and args.principal:
            number_of_payments(int(args.payment), float(args.interest), int(args.principal))
    elif args.type == 'diff' and not args.payment:
        differentiate_payment(float(args.interest), int(args.periods), int(args.principal))
    else:
        print('Incorrect parameters')


if __name__ == '__main__':
    main()
