import pickle
import Portfolio_Core


def save_portfolio(portfolio_obj):
    with open('{}_portfolio', 'wb') as output:
        pickle.dump(portfolio_obj, output, pickle.HIGHEST_PROTOCOL)


def load_portfolio(file_path):
    with open(file_path, 'rb') as pickle_input:
        portfolio = pickle.load(pickle_input)
    return portfolio


def main():
    pass


if __name__ == '__main__':
    main()
