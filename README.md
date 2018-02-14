# donation-analytics
Approach: I read the records from the stream and for each record, store the donor (name, zipcode) in a (donor) hash table that maps it to the (year, receiverID) pair if the donor does not exist in the hash table. Since the donor wasn't in the hash table, it's not a repeat donor so we don't need to write anything to the output file. If the donor exists in the donor hash table, but if the date of the stored transaction is more recent in time than that of the current transaction, we don't treat it as a repeat donor. As mentioned in the FAQ, we don't need to go back and change anything. So because the new transaction occurs before the stored transaction in time, we replace the stored transaction with the new transaction's details. The old transaction (the one which was stored before) isn't required anymore; all we need to know is the next time we come across this donor with a transaction date that's more recent in time compared to the stored one (the older in time between the first two transactions), it's a repeat donor. So we store the older (in time) transaction in the donor hash table. Since we're not changing anything in this case, we just update the entry in the hash table without writing anything to the output file. If the donor exists in the donor hash table and the date of the stored transaction is from a year that's before the current transaction's year (in time), it's a repeat donor. So we need to write to the output file. Among the fields we need to write to the output, we already have the receiver's id, donor's zipcode, and the year of the transaction. We also need the receiver's running percentile of contributions, the number of transactions, and the total amount received from repeat donors from this (transaction's) zipcode and this (transaction's) year. So we use another (receiver) hash table to store the mapping from the (receiverID, year, zipcode) tuple to the list of amounts from each of the transactions. We could have just stored the total amount and number of transactions but we also need the running percentile, and to compute this, we need the amount received in each of the transactions. Using the nearest rank method, we find out what amount exactly this percentile corresponds to, i.e. we need kth smallest amount in the list of amounts. So using nearest-rank method we find k. If the amounts are stored in a list, we will have to sort the data to find the kth smallest element which has a complexity of O(nlog(n)). We could use a modification of quicksort (quickselect) algorithm to find the kth smallest element. This has an average complexity of O(n) but a worst-case performance of O(n^2) which isn't good. So instead of using a list, I use a Binary Search Tree to store the amounts since the nodes' relative ordering can be taken advantage of to find the kth smallest element. Inserting an amount into the tree has average complexity of O(logn) and finding the kth smallest element (searching) also has an average complexity of O(logn). The worst cases for both insertion and search are O(n) each. This structure splits the work between insertion and search unlike a list which has fast appends but very poor search performance. Since every time we insert into the BST the amount passes through the root node, the root node can keep track of the number of nodes (transactions from repeat donors) as well as the total amount received from repeat donors. So we first insert the current transaction amount into the tree and then find the kth smallest amount (running percentile) along with the number of transactions and the total amount (from root node). We then write all of these values to the output file.

I use a config.py file which configures the path to the input and output files. This is OS-agnostic. I make use of datetime library (to check if date is valid), math (ceil() method for nearest-rank method), os and sys (to find paths).

I have a separate tests directory along with the given src, input, output directories. I make use of pytest for unit tests. It can be executed by going into tests directory and using the command: 
pytest.
insight_testsuite also works.

Initially, I thought that if a donor's transactions are out of order, i.e. if an old transaction (in time) is read after a more recent transaction, then this recent transaction (in time) should be considered as a transaction from a repeat donor. If that is the case, the donor hash table can map donor (donor, zipcode) to a heap consisting of all of the donor's transactions arranged based on transaction dates. So if a transaction isn't from the oldest year it is considered to be a repeat donor transaction. Except for the oldest year, all the others would be repeat donor transactions. The FAQ is vague but it says I don't need to go back and change anything and I should consider every transaction as a new transaction without considering the stored transaction again.

Sorry for the delay
