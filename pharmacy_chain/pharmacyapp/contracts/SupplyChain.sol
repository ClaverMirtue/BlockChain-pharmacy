// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {
    struct Medicine {
        string name;
        address manufacturer;
        address distributor;
        address pharmacy;
        uint256 quantity;
        string status;
        bool isActive;
    }

    mapping(uint256 => Medicine) public medicines;
    uint256 public medicineCount;

    event MedicineAdded(uint256 indexed medicineId, string name, address manufacturer);
    event StatusUpdated(uint256 indexed medicineId, string newStatus);
    event MedicineTransferred(uint256 indexed medicineId, address from, address to);

    function addMedicine(
        string memory _name,
        address _manufacturer,
        address _distributor,
        address _pharmacy,
        uint256 _quantity
    ) public returns (uint256) {
        medicineCount++;
        medicines[medicineCount] = Medicine({
            name: _name,
            manufacturer: _manufacturer,
            distributor: _distributor,
            pharmacy: _pharmacy,
            quantity: _quantity,
            status: "pending",
            isActive: true
        });

        emit MedicineAdded(medicineCount, _name, _manufacturer);
        return medicineCount;
    }

    function updateStatus(uint256 _medicineId, string memory _newStatus) public {
        require(medicines[_medicineId].isActive, "Medicine not active");
        require(
            msg.sender == medicines[_medicineId].manufacturer ||
            msg.sender == medicines[_medicineId].distributor ||
            msg.sender == medicines[_medicineId].pharmacy,
            "Not authorized"
        );

        medicines[_medicineId].status = _newStatus;
        emit StatusUpdated(_medicineId, _newStatus);
    }

    function transferMedicine(
        uint256 _medicineId,
        address _from,
        address _to
    ) public {
        require(medicines[_medicineId].isActive, "Medicine not active");
        require(
            msg.sender == medicines[_medicineId].manufacturer ||
            msg.sender == medicines[_medicineId].distributor ||
            msg.sender == medicines[_medicineId].pharmacy,
            "Not authorized"
        );

        if (_from == medicines[_medicineId].manufacturer) {
            require(_to == medicines[_medicineId].distributor, "Invalid transfer");
        } else if (_from == medicines[_medicineId].distributor) {
            require(_to == medicines[_medicineId].pharmacy, "Invalid transfer");
        }

        emit MedicineTransferred(_medicineId, _from, _to);
    }

    function getMedicine(uint256 _medicineId)
        public
        view
        returns (
            string memory name,
            address manufacturer,
            address distributor,
            address pharmacy,
            uint256 quantity,
            string memory status,
            bool isActive
        )
    {
        Medicine memory medicine = medicines[_medicineId];
        return (
            medicine.name,
            medicine.manufacturer,
            medicine.distributor,
            medicine.pharmacy,
            medicine.quantity,
            medicine.status,
            medicine.isActive
        );
    }
} 