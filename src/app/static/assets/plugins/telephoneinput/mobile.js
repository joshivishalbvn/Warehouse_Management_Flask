function format_phone_number(obj, ev) {
    let phoneNumber = $(obj).val().replace(/\D/g, ''); // Remove all non-digit characters
    console.log(phoneNumber)

    // Auto-format the number as 123-456-7890
    if (phoneNumber.length > 3) {
        phoneNumber = phoneNumber.slice(0, 3) + "-" + phoneNumber.slice(3);
    }
    if (phoneNumber.length > 7) {
        phoneNumber = phoneNumber.slice(0, 7) + "-" + phoneNumber.slice(7);
    }
    if (phoneNumber.length > 12) {
        phoneNumber = phoneNumber.slice(0, -1);
    }

    // Set the formatted value back to the input field
    $(obj).val(phoneNumber);
};

// onkeyup="format_phone_number(this,event);"