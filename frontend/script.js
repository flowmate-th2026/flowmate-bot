async function loadDashboard() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/dashboard");
        const data = await response.json();

        document.getElementById("sales-value").textContent =
            `฿${Number(data.sales).toLocaleString()}`;

        document.getElementById("expense-value").textContent =
            `฿${Number(data.expense).toLocaleString()}`;

        document.getElementById("profit-value").textContent =
            `฿${Number(data.profit).toLocaleString()}`;

        document.getElementById("customers-value").textContent =
            `${Number(data.customers).toLocaleString()} คน`;

        const topProducts = document.getElementById("top-products");

        if (topProducts) {
            if (data.top_products && data.top_products.length > 0) {
                topProducts.innerHTML = data.top_products
                    .slice(0, 3)
                    .map((product, index) => {
                        const medals = ["🥇", "🥈", "🥉"];

                        return `
                            <div class="top-product-item">
                                <span>${medals[index] || "🏅"} ${product.product_name}</span>
                                <strong>
                                    ${product.quantity} ชิ้น · ฿${Number(product.amount).toLocaleString()}
                                </strong>
                            </div>
                        `;
                    })
                    .join("");
            } else {
                topProducts.innerHTML = `
                    <div class="top-product-empty">
                        ยังไม่มีข้อมูลสินค้าขายดีวันนี้
                    </div>
                `;
            }
        }   


        const latestTransactions = document.getElementById("latest-transactions");

if (latestTransactions) {
    const transactions = [];

    // ยอดขายล่าสุด
    (data.latest_sales || []).forEach((item) => {
        transactions.push({
            type: "sale",
            icon: "💰",
            title: "ยอดขาย",
            detail: `฿${Number(item.amount).toLocaleString()}`,
            time: item.time || ""
        });
    });

    // ค่าใช้จ่ายล่าสุด
    (data.latest_expenses || []).forEach((item) => {
        transactions.push({
            type: "expense",
            icon: "💸",
            title: item.description || "ค่าใช้จ่าย",
            detail: `฿${Number(item.amount).toLocaleString()}`,
            time: item.time || ""
        });
    });

    // ลูกค้าล่าสุด
    (data.latest_customers || []).forEach((item) => {
        transactions.push({
            type: "customer",
            icon: "👥",
            title: "ลูกค้า",
            detail: `${Number(item.customer_count).toLocaleString()} คน`,
            time: item.time || ""
        });
    });

    // เรียงรายการใหม่สุดก่อน
    transactions.sort((a, b) =>
        b.time.localeCompare(a.time)
    );

    if (transactions.length > 0) {
        latestTransactions.innerHTML = transactions
            .slice(0, 5)
            .map((item) => `
                <div class="latest-item ${item.type}">
                    <div class="latest-icon">
                        ${item.icon}
                    </div>

                    <div class="latest-info">
                        <strong>${item.title}</strong>
                        <small>${item.time || "-"}</small>
                    </div>

                    <div class="latest-value">
                        ${item.detail}
                    </div>
                </div>
            `)
            .join("");
    } else {
        latestTransactions.innerHTML = `
            <div class="latest-empty">
                ยังไม่มีรายการวันนี้
            </div>
        `;
    }
}

        console.log("Dashboard updated:", data);
    } catch (error) {
        console.error("โหลดข้อมูล Dashboard ไม่สำเร็จ:", error);
    }
}

loadDashboard();

const recordButton = document.getElementById("record-button");
const recordModal = document.getElementById("record-modal");
const closeRecordModal = document.getElementById("close-record-modal");

if (recordButton && recordModal) {
    recordButton.addEventListener("click", () => {
        recordModal.classList.add("show");
    });
}

if (closeRecordModal && recordModal) {
    closeRecordModal.addEventListener("click", () => {
        recordModal.classList.remove("show");
    });
}

if (recordModal) {
    recordModal.addEventListener("click", (event) => {
        if (event.target === recordModal) {
            recordModal.classList.remove("show");
        }
    });
}

const salesRecordOption = document.getElementById("sales-record-option");
const recordOptions = document.querySelector(".record-options");
const salesForm = document.getElementById("sales-form");
const backToRecordOptions = document.getElementById("back-to-record-options");

if (salesRecordOption && recordOptions && salesForm) {
    salesRecordOption.addEventListener("click", () => {
        recordOptions.classList.add("hide");
        salesForm.classList.add("show");
    });
}

if (backToRecordOptions && recordOptions && salesForm) {
    backToRecordOptions.addEventListener("click", () => {
        salesForm.classList.remove("show");
        recordOptions.classList.remove("hide");
    });
}

const submitSalesButton = document.getElementById("submit-sales");
const salesAmountInput = document.getElementById("sales-amount");

if (submitSalesButton && salesAmountInput) {
    submitSalesButton.addEventListener("click", async () => {
        const amount = Number(salesAmountInput.value);

        if (!amount || amount <= 0) {
            alert("กรุณากรอกยอดขายให้ถูกต้อง");
            return;
        }

        try {
            submitSalesButton.disabled = true;
            submitSalesButton.textContent = "กำลังบันทึก...";

            const response = await fetch("http://127.0.0.1:5000/api/sales", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    amount: amount
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "บันทึกยอดขายไม่สำเร็จ");
            }

            alert("บันทึกยอดขายสำเร็จ 🎉");

            salesAmountInput.value = "";

            await loadDashboard();

            salesForm.classList.remove("show");
            recordOptions.classList.remove("hide");

        } catch (error) {
            console.error("บันทึกยอดขายไม่สำเร็จ:", error);
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง");
        } finally {
            submitSalesButton.disabled = false;
            submitSalesButton.textContent = "บันทึกยอดขาย";
        }
    });
}

const expenseRecordOption = document.getElementById("expense-record-option");
const expenseForm = document.getElementById("expense-form");
const backToRecordOptionsExpense = document.getElementById(
    "back-to-record-options-expense"
);

if (expenseRecordOption && recordOptions && expenseForm) {
    expenseRecordOption.addEventListener("click", () => {
        recordOptions.classList.add("hide");
        expenseForm.classList.add("show");
    });
}

if (backToRecordOptionsExpense && recordOptions && expenseForm) {
    backToRecordOptionsExpense.addEventListener("click", () => {
        expenseForm.classList.remove("show");
        recordOptions.classList.remove("hide");
    });
}

const submitExpenseButton = document.getElementById("submit-expense");
const expenseAmountInput = document.getElementById("expense-amount");
const expenseDescriptionInput = document.getElementById("expense-description");

if (
    submitExpenseButton &&
    expenseAmountInput &&
    expenseDescriptionInput
) {
    submitExpenseButton.addEventListener("click", async () => {
        const amount = Number(expenseAmountInput.value);
        const description = expenseDescriptionInput.value.trim();

        if (!amount || amount <= 0) {
            alert("กรุณากรอกจำนวนเงินให้ถูกต้อง");
            return;
        }

        if (!description) {
            alert("กรุณากรอกรายละเอียดค่าใช้จ่าย");
            return;
        }

        try {
            submitExpenseButton.disabled = true;
            submitExpenseButton.textContent = "กำลังบันทึก...";

            const response = await fetch(
                "http://127.0.0.1:5000/api/expenses",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        amount: amount,
                        description: description
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.message || "บันทึกค่าใช้จ่ายไม่สำเร็จ"
                );
            }

            alert("บันทึกค่าใช้จ่ายสำเร็จ 🎉");

            expenseAmountInput.value = "";
            expenseDescriptionInput.value = "";

            await loadDashboard();

            expenseForm.classList.remove("show");
            recordOptions.classList.remove("hide");

        } catch (error) {
            console.error("บันทึกค่าใช้จ่ายไม่สำเร็จ:", error);
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง");
        } finally {
            submitExpenseButton.disabled = false;
            submitExpenseButton.textContent = "บันทึกค่าใช้จ่าย";
        }
    });
}

const customerRecordOption = document.getElementById("customer-record-option");
const customerForm = document.getElementById("customer-form");
const backToRecordOptionsCustomer = document.getElementById(
    "back-to-record-options-customer"
);

if (customerRecordOption && recordOptions && customerForm) {
    customerRecordOption.addEventListener("click", () => {
        recordOptions.classList.add("hide");
        customerForm.classList.add("show");
    });
}

if (
    backToRecordOptionsCustomer &&
    recordOptions &&
    customerForm
) {
    backToRecordOptionsCustomer.addEventListener("click", () => {
        customerForm.classList.remove("show");
        recordOptions.classList.remove("hide");
    });
}

const submitCustomerButton = document.getElementById("submit-customer");
const customerCountInput = document.getElementById("customer-count");

if (submitCustomerButton && customerCountInput) {
    submitCustomerButton.addEventListener("click", async () => {
        const customerCount = Number(customerCountInput.value);

        if (!customerCount || customerCount <= 0) {
            alert("กรุณากรอกจำนวนลูกค้าให้ถูกต้อง");
            return;
        }

        try {
            submitCustomerButton.disabled = true;
            submitCustomerButton.textContent = "กำลังบันทึก...";

            const response = await fetch(
                "http://127.0.0.1:5000/api/customers",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        customer_count: customerCount,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.message || "บันทึกลูกค้าไม่สำเร็จ");
            }

            alert("บันทึกลูกค้าสำเร็จ 🎉");

            customerCountInput.value = "";

            await loadDashboard();

            customerForm.classList.remove("show");
            recordOptions.classList.remove("hide");

        } catch (error) {
            console.error("บันทึกลูกค้าไม่สำเร็จ:", error);
            alert("เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง");
        } finally {
            submitCustomerButton.disabled = false;
            submitCustomerButton.textContent = "บันทึกลูกค้า";
        }
    });
}

const productRecordOption = document.getElementById("product-record-option");
const productForm = document.getElementById("product-form");
const backToRecordOptionsProduct = document.getElementById(
    "back-to-record-options-product"
);

if (productRecordOption && recordOptions && productForm) {
    productRecordOption.addEventListener("click", () => {
        recordOptions.classList.add("hide");
        productForm.classList.add("show");
    });
}

if (
    backToRecordOptionsProduct &&
    recordOptions &&
    productForm
) {
    backToRecordOptionsProduct.addEventListener("click", () => {
        productForm.classList.remove("show");
        recordOptions.classList.remove("hide");
    });
}

const submitProduct = document.getElementById("submit-product");

if (submitProduct) {
    submitProduct.addEventListener("click", async () => {
        const productName = document
            .getElementById("product-name")
            .value
            .trim();

        const quantity = Number(
            document.getElementById("product-quantity").value
        );

        const amount = Number(
            document.getElementById("product-amount").value
        );

        if (!productName) {
            alert("กรุณากรอกชื่อสินค้า");
            return;
        }

        if (!quantity || quantity <= 0) {
            alert("กรุณากรอกจำนวนสินค้าให้ถูกต้อง");
            return;
        }

        if (!amount || amount <= 0) {
            alert("กรุณากรอกยอดขายรวมให้ถูกต้อง");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/api/products", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    product_name: productName,
                    quantity: quantity,
                    amount: amount,
                }),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                alert(data.message || "ไม่สามารถบันทึกการขายสินค้าได้");
                return;
            }

            alert("✅ บันทึกการขายสินค้าสำเร็จ");

            document.getElementById("product-name").value = "";
            document.getElementById("product-quantity").value = "0";
            document.getElementById("product-amount").value = "";

            productForm.classList.remove("show");
            recordModal.classList.remove("show");

            loadDashboard();
        } catch (error) {
            console.error(error);
            alert("เกิดข้อผิดพลาดในการบันทึกการขายสินค้า");
        }
    });
}