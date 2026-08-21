function validateNewEmployee(event) {
    let emp_no = document.getElementById('emp_no').value;
    let emp_name = document.getElementById('emp_name').value;
    let emp_sal = document.getElementById('emp_sal').value;
    let output_body = document.getElementById('output-body');
    
    output_body.innerHTML = "";
    output_body.className = "body";
    is_error = false;
    
    if(emp_no==0) {
        output_body.innerHTML = zero_ErrorIndicator('Employee No.')+"<br>";
        is_error = true;
    }
    else if(!positive_num.test(emp_no)) {
        output_body.innerHTML = positive_num_ErrorIndicator('Employee No')+"<br>";
        is_error = true;
    }

    if(!positive_num.test(emp_sal)) {
        output_body.innerHTML += positive_num_ErrorIndicator('Employee Salary');
        is_error = true;
    }

    if(is_error) {
        output_body.classList.add("error");
    }
    
    return !is_error;
}

const emp_pfpic = document.getElementById('emp_pfpic');
const emp_intvid = document.getElementById('emp_intvid');
const emp_resume = document.getElementById('emp_resume');
const MAX_PFPIC_FILESIZE_IN_KB = 100;
const MAX_INTVID_FILESIZE_IN_MB = 2;
const MAX_RESUME_FILESIZE_IN_KB = 100;

// Validate Profile Pic FileSize
emp_pfpic.addEventListener('change', function() {
    resetMsg();
    if(this.files.length > 0) {
        const curr_filesize_in_bytes = this.files[0].size;
        const max_filesize_in_bytes = MAX_PFPIC_FILESIZE_IN_KB * 1024;
        const error_msg = `Profile Pic File is too large! Max allowed size is ${MAX_PFPIC_FILESIZE_IN_KB}KB.`;
        if(curr_filesize_in_bytes > max_filesize_in_bytes) {
            this.value = '';
            showErrorMsg(error_msg);
        }
    }
})

// Validate Interview Video FileSize
emp_intvid.addEventListener('change', function() {
    resetMsg();
    if(this.files.length > 0) {
        const curr_filesize_in_bytes = this.files[0].size;
        const max_filesize_in_bytes = MAX_INTVID_FILESIZE_IN_MB * 1024 * 1024;
        const error_msg = `Interview Video File is too large! Max allowed size is ${MAX_INTVID_FILESIZE_IN_MB}MB.`;
        if(curr_filesize_in_bytes > max_filesize_in_bytes) {
            this.value = '';
            showErrorMsg(error_msg);
        }
    }
})

// Validate Resume FileSize
emp_resume.addEventListener('change', function() {
    resetMsg();
    if(this.files.length > 0) {
        const curr_filesize_in_bytes = this.files[0].size;
        const max_filesize_in_bytes = MAX_RESUME_FILESIZE_IN_KB * 1024;
        const error_msg = `Resume File is too large! Max allowed size is ${MAX_RESUME_FILESIZE_IN_KB}KB.`;
        if(curr_filesize_in_bytes > max_filesize_in_bytes) {
            this.value = '';
            showErrorMsg(error_msg);
        }
    }
})

const output_body = document.getElementById('output-body');
function resetMsg() {
    output_body.className = "body";
    output_body.innerHTML = "";
}
function showErrorMsg(error_msg) {
    output_body.classList.add("error");
    output_body.innerHTML = error_msg;
}