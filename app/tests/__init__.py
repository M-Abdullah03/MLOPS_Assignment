

class BankAccount:
    def _init_(self, owner):
        self.owner = owner
        self.balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return self.balance
        return "Invalid amount"

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return self.balance
        return "Insufficient funds"

accounts = {}

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    owner = data.get("owner")
    if owner in accounts:
        return jsonify({"message": "Account already exists"}), 400
    accounts[owner] = BankAccount(owner)
    return jsonify({"message": "Account created successfully"}), 201

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    owner = data.get("owner")
    amount = data.get("amount")
    if owner not in accounts:
        return jsonify({"message": "Account not found"}), 404
    balance = accounts[owner].deposit(amount)
    return jsonify({"balance": balance})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    owner = data.get("owner")
    amount = data.get("amount")
    if owner not in accounts:
        return jsonify({"message": "Account not found"}), 404
    balance = accounts[owner].withdraw(amount)
    return jsonify({"balance": balance})

if _name_ == "_main_":
    app.run(debug=True)