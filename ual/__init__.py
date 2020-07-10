import re

# Many of these instructions have multiple forms, which we don't adequately handle. Fixing this is left as an exercise to the reader.
instrs = {
    "ADC": [
        {
            "instr": "ADC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889307327.htm",
            "short": "Add with Carry",
        }
    ],
    "ADD": [
        {
            "instr": "ADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889841927.htm",
            "short": "Add",
        }
    ],
    "ADR": [
        {
            "instr": "ADR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889307327.htm",
            "short": "Load program or register-relative address (short range)",
        }
    ],
    "ADRL": [
        {
            "instr": "ADRL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889901839.htm",
            "short": "Load program or register-relative address (medium range)",
        }
    ],
    "AND": [
        {
            "instr": "AND",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889912421.htm",
            "short": "Logical AND",
        }
    ],
    "ASR": [
        {
            "instr": "ASR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889924482.htm",
            "short": "Arithmetic Shift Right",
        }
    ],
    "B": [
        {
            "instr": "B",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889934568.htm",
            "short": "Branch",
        }
    ],
    "BFC": [
        {
            "instr": "BFC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889942851.htm",
            "short": "Bit Field Clear and Insert",
        }
    ],
    "BFI": [
        {
            "instr": "BFI",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889950424.htm",
            "short": "Bit Field Clear and Insert",
        }
    ],
    "BIC": [
        {
            "instr": "BIC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889958629.htm",
            "short": "Bit Clear",
        }
    ],
    "BKPT": [
        {
            "instr": "BKPT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889966212.htm",
            "short": "Software breakpoint",
        }
    ],
    "BL": [
        {
            "instr": "BL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889981170.htm",
            "short": "Branch with Link",
        }
    ],
    "BLX": [
        {
            "instr": "BLX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889989549.htm",
            "short": "Branch with Link, change instruction set, Branch with Link and Exchange (Non-secure)",
        }
    ],
    "BLXNS": [
        {
            "instr": "BLXNS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889989549.htm",
            "short": "Branch with Link, change instruction set, Branch with Link and Exchange (Non-secure)",
        }
    ],
    "BX": [
        {
            "instr": "BX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889997181.htm",
            "short": "Branch, change instruction set, Branch and Exchange (Non-secure)",
        }
    ],
    "BXNS": [
        {
            "instr": "BXNS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889997181.htm",
            "short": "Branch, change instruction set, Branch and Exchange (Non-secure)",
        }
    ],
    "CBNZ": [
        {
            "instr": "CBNZ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890021484.htm",
            "short": "Compare and Branch if {Non}Zero",
        }
    ],
    "CBZ": [
        {
            "instr": "CBZ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890021484.htm",
            "short": "Compare and Branch if {Non}Zero",
        }
    ],
    "CDP": [
        {
            "instr": "CDP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890035506.htm",
            "short": "Coprocessor Data Processing operation",
        }
    ],
    "CDP2": [
        {
            "instr": "CDP2",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890035506.htm",
            "short": "Coprocessor Data Processing operation",
        }
    ],
    "CLREX": [
        {
            "instr": "CLREX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890046924.htm",
            "short": "Clear Exclusive",
        }
    ],
    "CLZ": [
        {
            "instr": "CLZ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890055713.htm",
            "short": "Count leading zeros",
        }
    ],
    "CMN": [
        {
            "instr": "CMN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890065626.htm",
            "short": "Compare Negative",
        }
    ],
    "CMP": [
        {
            "instr": "CMP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890065626.htm",
            "short": "Compare",
        }
    ],
    "CPS": [
        {
            "instr": "CPS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890075641.htm",
            "short": "Change Processor State",
        }
    ],
    "CPY": [
        {
            "instr": "CPY",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890087968.htm",
            "short": "Copy",
        }
    ],
    "CRC32": [
        {
            "instr": "CRC32",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_awi1476352818103.htm",
            "short": "CRC32",
        }
    ],
    "CRC32C": [
        {
            "instr": "CRC32C",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_qwe1476352818998.htm",
            "short": "CRC32C",
        }
    ],
    "DBG": [
        {
            "instr": "DBG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890104002.htm",
            "short": "Debug",
        }
    ],
    "DCPS1": [
        {
            "instr": "DCPS1",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890075641.htm",
            "short": "Debug switch to exception level 1",
        }
    ],
    "DCPS2": [
        {
            "instr": "DCPS2",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890075641.htm",
            "short": "Debug switch to exception level 2",
        }
    ],
    "DCPS3": [
        {
            "instr": "DCPS3",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890075641.htm",
            "short": "Debug switch to exception level 3",
        }
    ],
    "DMB": [
        {
            "instr": "DMB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890114571.htm",
            "short": "Data Memory Barrier",
        }
    ],
    "DSB": [
        {
            "instr": "DSB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890123364.htm",
            "short": "Data Synchronization Barrier",
        },
        {
            "instr": "DSB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890123364.htm",
            "short": "Data Synchronization Barrier",
        },
    ],
    "EOR": [
        {
            "instr": "EOR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890133290.htm",
            "short": "Exclusive OR",
        }
    ],
    "ERET": [
        {
            "instr": "ERET",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890145994.htm",
            "short": "Exception Return",
        }
    ],
    "ESB": [
        {
            "instr": "ESB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_wpv1476352823512.htm",
            "short": "Error Synchronization Barrier",
        }
    ],
    "FLDMDBX": [
        {
            "instr": "FLDMDBX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_kqy1476352931459.htm",
            "short": "FLDMX",
        }
    ],
    "FLDMIAX": [
        {
            "instr": "FLDMIAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_kqy1476352931459.htm",
            "short": "FLDMX",
        }
    ],
    "FSTMDBX": [
        {
            "instr": "FSTMDBX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_fgf1476352931779.htm",
            "short": "FSTMX",
        }
    ],
    "FSTMIAX": [
        {
            "instr": "FSTMIAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_fgf1476352931779.htm",
            "short": "FSTMX",
        }
    ],
    "HLT": [
        {
            "instr": "HLT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425564187099.htm",
            "short": "Halting breakpoint",
        }
    ],
    "HVC": [
        {
            "instr": "HVC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890193980.htm",
            "short": "Hypervisor Call",
        }
    ],
    "ISB": [
        {
            "instr": "ISB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890205000.htm",
            "short": "Instruction Synchronization Barrier",
        }
    ],
    "IT": [
        {
            "instr": "IT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890218120.htm",
            "short": "If-Then",
        }
    ],
    "LDA": [
        {
            "instr": "LDA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429112691581.htm",
            "short": "Load-Acquire Register Word",
        }
    ],
    "LDAB": [
        {
            "instr": "LDAB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429112691581.htm",
            "short": "Load-Acquire Register Byte",
        }
    ],
    "LDAEX": [
        {
            "instr": "LDAEX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433203404.htm",
            "short": "Load-Acquire Register Exclusive Word",
        }
    ],
    "LDAEXB": [
        {
            "instr": "LDAEXB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433203404.htm",
            "short": "Load-Acquire Register Exclusive Byte",
        }
    ],
    "LDAEXD": [
        {
            "instr": "LDAEXD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433203404.htm",
            "short": "Load-Acquire Register Exclusive Doubleword",
        }
    ],
    "LDAEXH": [
        {
            "instr": "LDAEXH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433203404.htm",
            "short": "Load-Acquire Register Exclusive Halfword",
        }
    ],
    "LDAH": [
        {
            "instr": "LDAH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429112691581.htm",
            "short": "Load-Acquire Register Halfword",
        }
    ],
    "LDC": [
        {
            "instr": "LDC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890230375.htm",
            "short": "Load Coprocessor",
        }
    ],
    "LDC2": [
        {
            "instr": "LDC2",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890230375.htm",
            "short": "Load Coprocessor",
        }
    ],
    "LDM": [
        {
            "instr": "LDM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890240379.htm",
            "short": "Load Multiple registers",
        }
    ],
    "LDR": [
        {
            "instr": "LDR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with word",
        },
        {
            "instr": "LDR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890292360.htm",
            "short": "Load Register pseudo-instruction",
        },
    ],
    "LDRB": [
        {
            "instr": "LDRB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with Byte",
        }
    ],
    "LDRBT": [
        {
            "instr": "LDRBT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901492903.htm",
            "short": "Load Register with Byte, user mode",
        }
    ],
    "LDRD": [
        {
            "instr": "LDRD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Registers with two words",
        }
    ],
    "LDREX": [
        {
            "instr": "LDREX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890318276.htm",
            "short": "Load Register Exclusive Word",
        }
    ],
    "LDREXB": [
        {
            "instr": "LDREXB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890318276.htm",
            "short": "Load Register Exclusive Byte",
        }
    ],
    "LDREXD": [
        {
            "instr": "LDREXD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890318276.htm",
            "short": "Load Register Exclusive Doubleword",
        }
    ],
    "LDREXH": [
        {
            "instr": "LDREXH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890318276.htm",
            "short": "Load Register Exclusive Halfword",
        }
    ],
    "LDRH": [
        {
            "instr": "LDRH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with Halfword",
        }
    ],
    "LDRHT": [
        {
            "instr": "LDRHT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with Halfword, user mode",
        }
    ],
    "LDRSB": [
        {
            "instr": "LDRSB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890123364.htm",
            "short": "Load Register with Signed Byte",
        }
    ],
    "LDRSBT": [
        {
            "instr": "LDRSBT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890123364.htm",
            "short": "Load Register with Signed Byte, user mode",
        }
    ],
    "LDRSH": [
        {
            "instr": "LDRSH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with Signed Halfword",
        }
    ],
    "LDRSHT": [
        {
            "instr": "LDRSHT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with Signed Halfword, user mode",
        }
    ],
    "LDRT": [
        {
            "instr": "LDRT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Load Register with word, user mode",
        }
    ],
    "LSL": [
        {
            "instr": "LSL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890373464.htm",
            "short": "Logical Shift Left",
        }
    ],
    "LSR": [
        {
            "instr": "LSR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890383924.htm",
            "short": "Logical Shift Right",
        }
    ],
    "MCR": [
        {
            "instr": "MCR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890395091.htm",
            "short": "Move from Register to Coprocessor",
        }
    ],
    "MCRR": [
        {
            "instr": "MCRR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890404678.htm",
            "short": "Move from Registers to Coprocessor",
        }
    ],
    "MLA": [
        {
            "instr": "MLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890415957.htm",
            "short": "Multiply Accumulate",
        }
    ],
    "MLS": [
        {
            "instr": "MLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890428981.htm",
            "short": "Multiply and Subtract",
        }
    ],
    "MOV": [
        {
            "instr": "MOV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890440026.htm",
            "short": "Move",
        }
    ],
    "MOV32": [
        {
            "instr": "MOV32",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890455346.htm",
            "short": "Move 32-bit immediate to register",
        }
    ],
    "MOVT": [
        {
            "instr": "MOVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890480348.htm",
            "short": "Move Top",
        }
    ],
    "MRC": [
        {
            "instr": "MRC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890493551.htm",
            "short": "Move from Coprocessor to Register",
        }
    ],
    "MRRC": [
        {
            "instr": "MRRC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890504536.htm",
            "short": "Move from Coprocessor to Registers",
        }
    ],
    "MRS": [
        {
            "instr": "MRS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433211144.htm",
            "short": "Move from PSR to Register",
        },
        {
            "instr": "MRS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890292360.htm",
            "short": "Move from system Coprocessor to Register",
        },
    ],
    "MSR": [
        {
            "instr": "MSR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424868721235.htm",
            "short": "Move from Register to PSR",
        },
        {
            "instr": "MSR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890292360.htm",
            "short": "Move from Register to system Coprocessor",
        },
    ],
    "MUL": [
        {
            "instr": "MUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898077663.htm",
            "short": "Multiply",
        }
    ],
    "MVN": [
        {
            "instr": "MVN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898090605.htm",
            "short": "Move Not",
        }
    ],
    "NEG": [
        {
            "instr": "NEG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898099992.htm",
            "short": "Negate",
        }
    ],
    "NOP": [
        {
            "instr": "NOP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898111637.htm",
            "short": "No Operation",
        }
    ],
    "ORN": [
        {
            "instr": "ORN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890133290.htm",
            "short": "Logical OR NOT",
        }
    ],
    "ORR": [
        {
            "instr": "ORR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898123112.htm",
            "short": "Logical OR",
        }
    ],
    "PKHBT": [
        {
            "instr": "PKHBT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898999025.htm",
            "short": "Pack Halfwords",
        }
    ],
    "PKHTB": [
        {
            "instr": "PKHTB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898999025.htm",
            "short": "Pack Halfwords",
        }
    ],
    "PLD": [
        {
            "instr": "PLD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899018492.htm",
            "short": "Preload Data",
        }
    ],
    "PLDW": [
        {
            "instr": "PLDW",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899018492.htm",
            "short": "Preload Data with intent to Write",
        }
    ],
    "PLI": [
        {
            "instr": "PLI",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899018492.htm",
            "short": "Preload Instruction",
        }
    ],
    "POP": [
        {
            "instr": "POP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899030586.htm",
            "short": "POP registers from stack",
        }
    ],
    "PUSH": [
        {
            "instr": "PUSH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899044621.htm",
            "short": "PUSH registers to stack",
        }
    ],
    "QADD": [
        {
            "instr": "QADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899860328.htm",
            "short": "Saturating arithmetic",
        }
    ],
    "QADD16": [
        {
            "instr": "QADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899883374.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "QADD8": [
        {
            "instr": "QADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899871217.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "QASX": [
        {
            "instr": "QASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899892360.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "QDADD": [
        {
            "instr": "QDADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899904388.htm",
            "short": "Saturating arithmetic",
        }
    ],
    "QDSUB": [
        {
            "instr": "QDSUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425899914201.htm",
            "short": "Saturating arithmetic",
        }
    ],
    "QSAX": [
        {
            "instr": "QSAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901210287.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "QSUB": [
        {
            "instr": "QSUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901227555.htm",
            "short": "Saturating arithmetic",
        }
    ],
    "QSUB16": [
        {
            "instr": "QSUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901246838.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "QSUB8": [
        {
            "instr": "QSUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901237598.htm",
            "short": "Parallel signed saturating arithmetic",
        }
    ],
    "RBIT": [
        {
            "instr": "RBIT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901492903.htm",
            "short": "Reverse Bits",
        }
    ],
    "REV": [
        {
            "instr": "REV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901506568.htm",
            "short": "Reverse byte order",
        }
    ],
    "REV16": [
        {
            "instr": "REV16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901520514.htm",
            "short": "Reverse byte order",
        }
    ],
    "REVSH": [
        {
            "instr": "REVSH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901584041.htm",
            "short": "Reverse byte order",
        }
    ],
    "RFE": [
        {
            "instr": "RFE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901533481.htm",
            "short": "Return From Exception",
        }
    ],
    "ROR": [
        {
            "instr": "ROR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901541467.htm",
            "short": "Rotate Right Register",
        }
    ],
    "RRX": [
        {
            "instr": "RRX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901551183.htm",
            "short": "Rotate Right with Extend",
        }
    ],
    "RSB": [
        {
            "instr": "RSB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901593052.htm",
            "short": "Reverse Subtract",
        }
    ],
    "RSC": [
        {
            "instr": "RSC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901602609.htm",
            "short": "Reverse Subtract with Carry",
        }
    ],
    "SADD16": [
        {
            "instr": "SADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906530739.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "SADD8": [
        {
            "instr": "SADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906514185.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "SASX": [
        {
            "instr": "SASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906539458.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "SBC": [
        {
            "instr": "SBC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906548297.htm",
            "short": "Subtract with Carry",
        }
    ],
    "SBFX": [
        {
            "instr": "SBFX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906593664.htm",
            "short": "Signed Bit Field eXtract",
        }
    ],
    "SDIV": [
        {
            "instr": "SDIV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906604697.htm",
            "short": "Signed Divide",
        }
    ],
    "SEL": [
        {
            "instr": "SEL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906625495.htm",
            "short": "Select bytes according to APSR GE flags",
        }
    ],
    "SETEND": [
        {
            "instr": "SETEND",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906645592.htm",
            "short": "Set Endianness for memory accesses",
        }
    ],
    "SETPAN": [
        {
            "instr": "SETPAN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_eai1476352878905.htm",
            "short": "Set Privileged Access Never",
        }
    ],
    "SEV": [
        {
            "instr": "SEV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425906657222.htm",
            "short": "Set Event",
        }
    ],
    "SEVL": [
        {
            "instr": "SEVL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429177774796.htm",
            "short": "Set Event Locally",
        }
    ],
    "SG": [
        {
            "instr": "SG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1447175165109.htm",
            "short": "Secure Gateway",
        }
    ],
    "SHADD16": [
        {
            "instr": "SHADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910454133.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SHADD8": [
        {
            "instr": "SHADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910435007.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SHASX": [
        {
            "instr": "SHASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910463798.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SHSAX": [
        {
            "instr": "SHSAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910473096.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SHSUB16": [
        {
            "instr": "SHSUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910559031.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SHSUB8": [
        {
            "instr": "SHSUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910482480.htm",
            "short": "Parallel Signed Halving arithmetic",
        }
    ],
    "SMC": [
        {
            "instr": "SMC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910897272.htm",
            "short": "Secure Monitor Call",
        }
    ],
    "SMLAD": [
        {
            "instr": "SMLAD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910917679.htm",
            "short": "Dual Signed Multiply Accumulate",
        }
    ],
    "SMLAL": [
        {
            "instr": "SMLAL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910926465.htm",
            "short": "Signed Multiply Accumulate (64 <= 64 + 32 x 32)",
        }
    ],
    "SMLALD": [
        {
            "instr": "SMLALD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910935569.htm",
            "short": "Dual Signed Multiply Accumulate Long",
        }
    ],
    "SMLALxy": [
        {
            "instr": "SMLALxy",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910945100.htm",
            "short": "Signed Multiply Accumulate (64 <= 64 + 16 x 16)",
        }
    ],
    "SMLAWy": [
        {
            "instr": "SMLAWy",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910954185.htm",
            "short": "Signed Multiply with Accumulate (32 <= 32 x 16 + 32)",
        }
    ],
    "SMLAxy": [
        {
            "instr": "SMLAxy",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910907132.htm",
            "short": "Signed Multiply with Accumulate (32 <= 16 x 16 + 32)",
        }
    ],
    "SMLSD": [
        {
            "instr": "SMLSD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910962669.htm",
            "short": "Dual Signed Multiply Subtract Accumulate",
        }
    ],
    "SMLSLD": [
        {
            "instr": "SMLSLD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910971648.htm",
            "short": "Dual Signed Multiply Subtract Accumulate Long",
        }
    ],
    "SMMLA": [
        {
            "instr": "SMMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910984298.htm",
            "short": "Signed top word Multiply with Accumulate (32 <= TopWord(32 x 32 + 32))",
        }
    ],
    "SMMLS": [
        {
            "instr": "SMMLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425910992502.htm",
            "short": "Signed top word Multiply with Subtract (32 <= TopWord(32 - 32 x 32))",
        }
    ],
    "SMMUL": [
        {
            "instr": "SMMUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911003437.htm",
            "short": "Signed top word Multiply (32 <= TopWord(32 x 32))",
        }
    ],
    "SMUAD": [
        {
            "instr": "SMUAD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911015421.htm",
            "short": "Dual Signed Multiply and Add product",
        }
    ],
    "SMULL": [
        {
            "instr": "SMULL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911036135.htm",
            "short": "Signed Multiply (64 <= 32 x 32)",
        }
    ],
    "SMULWy": [
        {
            "instr": "SMULWy",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911044506.htm",
            "short": "Signed Multiply (32 <= 32 x 16)",
        }
    ],
    "SMULxy": [
        {
            "instr": "SMULxy",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911027047.htm",
            "short": "Signed Multiply (32 <= 16 x 16)",
        }
    ],
    "SMUSD": [
        {
            "instr": "SMUSD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911055519.htm",
            "short": "Dual Signed Multiply and Subtract product",
        }
    ],
    "SRS": [
        {
            "instr": "SRS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911938187.htm",
            "short": "Store Return State",
        }
    ],
    "SSAT": [
        {
            "instr": "SSAT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911950587.htm",
            "short": "Signed Saturate",
        }
    ],
    "SSAT16": [
        {
            "instr": "SSAT16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911959532.htm",
            "short": "Signed Saturate, parallel halfwords",
        }
    ],
    "SSAX": [
        {
            "instr": "SSAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425911968531.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "SSUB16": [
        {
            "instr": "SSUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425912033174.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "SSUB8": [
        {
            "instr": "SSUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425912022655.htm",
            "short": "Parallel Signed arithmetic",
        }
    ],
    "STC": [
        {
            "instr": "STC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890529837.htm",
            "short": "Store Coprocessor",
        }
    ],
    "STL": [
        {
            "instr": "STL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429113453813.htm",
            "short": "Store-Release Word",
        }
    ],
    "STLB": [
        {
            "instr": "STLB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429113453813.htm",
            "short": "Store-Release Byte",
        }
    ],
    "STLEX": [
        {
            "instr": "STLEX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890542287.htm",
            "short": "Store-Release Exclusive Word",
        }
    ],
    "STLEXB": [
        {
            "instr": "STLEXB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890542287.htm",
            "short": "Store-Release Exclusive Byte",
        }
    ],
    "STLEXD": [
        {
            "instr": "STLEXD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890542287.htm",
            "short": "Store-Release Exclusive Doubleword",
        }
    ],
    "STLEXH": [
        {
            "instr": "STLEXH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890542287.htm",
            "short": "Store-Release Exclusive Halfword",
        }
    ],
    "STLH": [
        {
            "instr": "STLH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1429113453813.htm",
            "short": "Store-Release Halfword",
        }
    ],
    "STM": [
        {
            "instr": "STM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890554593.htm",
            "short": "Store Multiple registers",
        }
    ],
    "STR": [
        {
            "instr": "STR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289990966.htm",
            "short": "Store Register with word",
        }
    ],
    "STRB": [
        {
            "instr": "STRB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914119973.htm",
            "short": "Store Register with Byte",
        }
    ],
    "STRBT": [
        {
            "instr": "STRBT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901492903.htm",
            "short": "Store Register with Byte, user mode",
        }
    ],
    "STRD": [
        {
            "instr": "STRD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289990966.htm",
            "short": "Store Registers with two words",
        }
    ],
    "STREX": [
        {
            "instr": "STREX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890604489.htm",
            "short": "Store Register Exclusive Word",
        }
    ],
    "STREXB": [
        {
            "instr": "STREXB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890604489.htm",
            "short": "Store Register Exclusive Byte",
        }
    ],
    "STREXD": [
        {
            "instr": "STREXD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890604489.htm",
            "short": "Store Register Exclusive Doubleword",
        }
    ],
    "STREXH": [
        {
            "instr": "STREXH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425890604489.htm",
            "short": "Store Register Exclusive Halfword",
        }
    ],
    "STRH": [
        {
            "instr": "STRH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914139870.htm",
            "short": "Store Register with Halfword",
        }
    ],
    "STRHT": [
        {
            "instr": "STRHT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914139870.htm",
            "short": "Store Register with Halfword, user mode",
        }
    ],
    "STRT": [
        {
            "instr": "STRT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289990966.htm",
            "short": "Store Register with word, user mode",
        }
    ],
    "SUB": [
        {
            "instr": "SUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914016900.htm",
            "short": "Subtract",
        }
    ],
    "SUBS": [
        {
            "instr": "SUBS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914041468.htm",
            "short": "Exception return, no stack",
        }
    ],
    "SVC": [
        {
            "instr": "SVC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914052313.htm",
            "short": "Supervisor Call",
        }
    ],
    "SXTAB": [
        {
            "instr": "SXTAB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914089623.htm",
            "short": "Signed extend, with Addition",
        }
    ],
    "SXTAB16": [
        {
            "instr": "SXTAB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914101520.htm",
            "short": "Signed extend, with Addition",
        }
    ],
    "SXTAH": [
        {
            "instr": "SXTAH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914111505.htm",
            "short": "Signed extend, with Addition",
        }
    ],
    "SXTB": [
        {
            "instr": "SXTB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914119973.htm",
            "short": "Signed extend",
        }
    ],
    "SXTB16": [
        {
            "instr": "SXTB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914128788.htm",
            "short": "Signed extend",
        }
    ],
    "SXTH": [
        {
            "instr": "SXTH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914139870.htm",
            "short": "Signed extend",
        }
    ],
    "SYS": [
        {
            "instr": "SYS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914149910.htm",
            "short": "Execute System coprocessor instruction",
        }
    ],
    "TBB": [
        {
            "instr": "TBB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914159689.htm",
            "short": "Table Branch Byte",
        }
    ],
    "TBH": [
        {
            "instr": "TBH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914159689.htm",
            "short": "Table Branch Halfword",
        }
    ],
    "TEQ": [
        {
            "instr": "TEQ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914168242.htm",
            "short": "Test Equivalence",
        }
    ],
    "TST": [
        {
            "instr": "TST",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425914177163.htm",
            "short": "Test",
        }
    ],
    "TT": [
        {
            "instr": "TT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1447175167080.htm",
            "short": "Test Target (Alternate Domain, Unprivileged)",
        }
    ],
    "TTA": [
        {
            "instr": "TTA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1447175167080.htm",
            "short": "Test Target (Alternate Domain, Unprivileged)",
        }
    ],
    "TTAT": [
        {
            "instr": "TTAT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1447175167080.htm",
            "short": "Test Target (Alternate Domain, Unprivileged)",
        }
    ],
    "TTT": [
        {
            "instr": "TTT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1447175167080.htm",
            "short": "Test Target (Alternate Domain, Unprivileged)",
        }
    ],
    "UADD16": [
        {
            "instr": "UADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425915350745.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "UADD8": [
        {
            "instr": "UADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425915337975.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "UASX": [
        {
            "instr": "UASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425915362627.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "UBFX": [
        {
            "instr": "UBFX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425915375380.htm",
            "short": "Unsigned Bit Field eXtract",
        }
    ],
    "UDF": [
        {
            "instr": "UDF",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_zme1476352914494.htm",
            "short": "Permanently Undefined",
        }
    ],
    "UDIV": [
        {
            "instr": "UDIV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425915385325.htm",
            "short": "Unsigned Divide",
        }
    ],
    "UHADD16": [
        {
            "instr": "UHADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916046129.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UHADD8": [
        {
            "instr": "UHADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916032545.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UHASX": [
        {
            "instr": "UHASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916058137.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UHSAX": [
        {
            "instr": "UHSAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916068035.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UHSUB16": [
        {
            "instr": "UHSUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916084548.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UHSUB8": [
        {
            "instr": "UHSUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916075981.htm",
            "short": "Parallel Unsigned Halving arithmetic",
        }
    ],
    "UMAAL": [
        {
            "instr": "UMAAL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916094062.htm",
            "short": "Unsigned Multiply Accumulate Accumulate Long",
        }
    ],
    "UMLAL": [
        {
            "instr": "UMLAL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916104084.htm",
            "short": "Unsigned Multiply Accumulate",
        }
    ],
    "UMULL": [
        {
            "instr": "UMULL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916119892.htm",
            "short": "Unsigned Multiply",
        }
    ],
    "UQADD16": [
        {
            "instr": "UQADD16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916577462.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "UQADD8": [
        {
            "instr": "UQADD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916563479.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "UQASX": [
        {
            "instr": "UQASX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916586427.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "UQSAX": [
        {
            "instr": "UQSAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916594735.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "UQSUB16": [
        {
            "instr": "UQSUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916613661.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "UQSUB8": [
        {
            "instr": "UQSUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916604231.htm",
            "short": "Parallel Unsigned Saturating arithmetic",
        }
    ],
    "USAD8": [
        {
            "instr": "USAD8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916622373.htm",
            "short": "Unsigned Sum of Absolute Differences",
        }
    ],
    "USADA8": [
        {
            "instr": "USADA8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916631159.htm",
            "short": "Accumulate Unsigned Sum of Absolute Differences",
        }
    ],
    "USAT": [
        {
            "instr": "USAT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916641790.htm",
            "short": "Unsigned Saturate",
        }
    ],
    "USAT16": [
        {
            "instr": "USAT16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916654170.htm",
            "short": "Unsigned Saturate, parallel halfwords",
        }
    ],
    "USAX": [
        {
            "instr": "USAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425916663991.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "USUB16": [
        {
            "instr": "USUB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917062704.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "USUB8": [
        {
            "instr": "USUB8",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917046103.htm",
            "short": "Parallel Unsigned arithmetic",
        }
    ],
    "UXTAB": [
        {
            "instr": "UXTAB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917070663.htm",
            "short": "Unsigned extend with Addition",
        }
    ],
    "UXTAB16": [
        {
            "instr": "UXTAB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917078324.htm",
            "short": "Unsigned extend with Addition",
        }
    ],
    "UXTAH": [
        {
            "instr": "UXTAH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917086082.htm",
            "short": "Unsigned extend with Addition",
        }
    ],
    "UXTB": [
        {
            "instr": "UXTB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917094057.htm",
            "short": "Unsigned extend",
        }
    ],
    "UXTB16": [
        {
            "instr": "UXTB16",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917102054.htm",
            "short": "Unsigned extend",
        }
    ],
    "UXTH": [
        {
            "instr": "UXTH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917110918.htm",
            "short": "Unsigned extend",
        }
    ],
    "VABA": [
        {
            "instr": "VABA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289938635.htm",
            "short": "Absolute difference and Accumulate",
        }
    ],
    "VABD": [
        {
            "instr": "VABD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289938965.htm",
            "short": "Absolute Difference",
        }
    ],
    "VABS": [
        {
            "instr": "VABS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289939344.htm",
            "short": "Absolute value",
        },
        {
            "instr": "VABS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289939344.htm",
            "short": "Absolute value",
        },
    ],
    "VACGE": [
        {
            "instr": "VACGE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Absolute Compare Greater than or Equal",
        }
    ],
    "VACGT": [
        {
            "instr": "VACGT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Absolute Compare Greater Than",
        }
    ],
    "VACLE": [
        {
            "instr": "VACLE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Absolute Compare Less than or Equal",
        }
    ],
    "VACLT": [
        {
            "instr": "VACLT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Absolute Compare Less Than (pseudo-instructions)",
        }
    ],
    "VADD": [
        {
            "instr": "VADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940984.htm",
            "short": "Add",
        },
        {
            "instr": "VADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940984.htm",
            "short": "Add",
        },
    ],
    "VADDHN": [
        {
            "instr": "VADDHN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289941334.htm",
            "short": "Add, select High half",
        }
    ],
    "VAND": [
        {
            "instr": "VAND",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889912421.htm",
            "short": "Bitwise AND",
        },
        {
            "instr": "VAND",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889912421.htm",
            "short": "Bitwise AND (pseudo-instruction)",
        },
    ],
    "VBIC": [
        {
            "instr": "VBIC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889958629.htm",
            "short": "Bitwise Bit Clear (register)",
        },
        {
            "instr": "VBIC",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425889958629.htm",
            "short": "Bitwise Bit Clear (immediate)",
        },
    ],
    "VBIF": [
        {
            "instr": "VBIF",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289943534.htm",
            "short": "Bitwise Insert if False",
        }
    ],
    "VBIT": [
        {
            "instr": "VBIT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289943884.htm",
            "short": "Bitwise Insert if True",
        }
    ],
    "VBSL": [
        {
            "instr": "VBSL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289944294.htm",
            "short": "Select",
        }
    ],
    "VCADD": [
        {
            "instr": "VCADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ydp1476352944870.htm",
            "short": "Vector Complex Add",
        }
    ],
    "VCEQ": [
        {
            "instr": "VCEQ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Equal",
        }
    ],
    "VCGE": [
        {
            "instr": "VCGE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Greater than or Equal",
        }
    ],
    "VCGT": [
        {
            "instr": "VCGT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Greater Than",
        }
    ],
    "VCLE": [
        {
            "instr": "VCLE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Less than or Equal",
        },
        {
            "instr": "VCLE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Less than or Equal",
        },
    ],
    "VCLS": [
        {
            "instr": "VCLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289947693.htm",
            "short": "Count Leading Sign bits",
        }
    ],
    "VCLT": [
        {
            "instr": "VCLT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Less Than",
        },
        {
            "instr": "VCLT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289940174.htm",
            "short": "Compare Less Than (pseudo-instruction)",
        },
    ],
    "VCLZ": [
        {
            "instr": "VCLZ",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289948783.htm",
            "short": "Count Leading Zeros",
        }
    ],
    "VCMLA": [
        {
            "instr": "VCMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_acv1476352950970.htm",
            "short": "Vector Complex Multiply Accumulate",
        }
    ],
    "VCMLA (by element)": [
        {
            "instr": "VCMLA (by element)",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_mkm1476352951310.htm",
            "short": "Vector Complex Multiply Accumulate (by element)",
        }
    ],
    "VCMP": [
        {
            "instr": "VCMP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289949173.htm",
            "short": "Compare",
        }
    ],
    "VCMPE": [
        {
            "instr": "VCMPE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289949173.htm",
            "short": "Compare",
        }
    ],
    "VCNT": [
        {
            "instr": "VCNT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289949533.htm",
            "short": "Count set bits",
        }
    ],
    "VCVT": [
        {
            "instr": "VCVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert fixed-point or integer to floating-point, floating-point to integer or fixed-point",
        },
        {
            "instr": "VCVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert floating-point to integer with directed rounding modes",
        },
        {
            "instr": "VCVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert between half-precision and single-precision floating-point numbers",
        },
        {
            "instr": "VCVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert between single-precision and double-precision",
        },
    ],
    "VCVTB": [
        {
            "instr": "VCVTB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert between half-precision and single-precision floating-point",
        }
    ],
    "VCVTT": [
        {
            "instr": "VCVTT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Convert between half-precision and single-precision floating-point",
        }
    ],
    "VDIV": [
        {
            "instr": "VDIV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289952072.htm",
            "short": "Divide",
        }
    ],
    "VDUP": [
        {
            "instr": "VDUP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289952392.htm",
            "short": "Duplicate scalar to all lanes of vector",
        }
    ],
    "VEOR": [
        {
            "instr": "VEOR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289952722.htm",
            "short": "Bitwise Exclusive OR",
        }
    ],
    "VEXT": [
        {
            "instr": "VEXT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953622.htm",
            "short": "Extract",
        }
    ],
    "VFMA": [
        {
            "instr": "VFMA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953962.htm",
            "short": "Fused Multiply Accumulate",
        },
        {
            "instr": "VFMA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953962.htm",
            "short": "Fused multiply accumulate",
        },
    ],
    "VFMS": [
        {
            "instr": "VFMS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953962.htm",
            "short": "Fused Multiply Subtract",
        },
        {
            "instr": "VFMS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953962.htm",
            "short": "Fused multiply subtract",
        },
    ],
    "VFNMA": [
        {
            "instr": "VFNMA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289954342.htm",
            "short": "Fused multiply accumulate with negation",
        }
    ],
    "VFNMS": [
        {
            "instr": "VFNMS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289953962.htm",
            "short": "Fused multiply subtract with negation",
        }
    ],
    "VHADD": [
        {
            "instr": "VHADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289954742.htm",
            "short": "Halving Add",
        }
    ],
    "VHSUB": [
        {
            "instr": "VHSUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289955132.htm",
            "short": "Halving Subtract",
        }
    ],
    "VJCVT": [
        {
            "instr": "VJCVT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ici1476352964675.htm",
            "short": "Javascript Convert to signed fixed-point, rounding toward Zero",
        }
    ],
    "VLD": [
        {
            "instr": "VLD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289956822.htm",
            "short": "Vector Load",
        }
    ],
    "VLDM": [
        {
            "instr": "VLDM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289956822.htm",
            "short": "Extension register load multiple",
        }
    ],
    "VLDR": [
        {
            "instr": "VLDR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289957202.htm",
            "short": "Extension register load",
        }
    ],
    "VLLDM": [
        {
            "instr": "VLLDM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_ibk1480518609451.htm",
            "short": "Floating-point Lazy Load Multiple",
        }
    ],
    "VLSTM": [
        {
            "instr": "VLSTM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_zth1480518611751.htm",
            "short": "Floating-point Lazy Store Multiple",
        }
    ],
    "VMAX": [
        {
            "instr": "VMAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958291.htm",
            "short": "Maximum",
        }
    ],
    "VMAXNM": [
        {
            "instr": "VMAXNM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433209634.htm",
            "short": "Maximum, consistent with IEEE 754-2008",
        },
        {
            "instr": "VMAXNM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433209634.htm",
            "short": "Maximum, Minimum, consistent with IEEE 754-2008",
        },
    ],
    "VMIN": [
        {
            "instr": "VMIN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958291.htm",
            "short": "Minimum",
        }
    ],
    "VMINNM": [
        {
            "instr": "VMINNM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433209634.htm",
            "short": "Minimum, consistent with IEEE 754-2008",
        },
        {
            "instr": "VMINNM",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433209634.htm",
            "short": "Maximum, Minimum, consistent with IEEE 754-2008",
        },
    ],
    "VMLA": [
        {
            "instr": "VMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958611.htm",
            "short": "Multiply Accumulate",
        },
        {
            "instr": "VMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958611.htm",
            "short": "Multiply Accumulate",
        },
        {
            "instr": "VMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958611.htm",
            "short": "Multiply accumulate",
        },
    ],
    "VMLS": [
        {
            "instr": "VMLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289960701.htm",
            "short": "Multiply Subtract (vector)",
        },
        {
            "instr": "VMLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289960701.htm",
            "short": "Multiply Subtract (by scalar)",
        },
        {
            "instr": "VMLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289960701.htm",
            "short": "Multiply subtract",
        },
    ],
    "VMOV": [
        {
            "instr": "VMOV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289964290.htm",
            "short": "Move (immediate)",
        },
        {
            "instr": "VMOV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289964290.htm",
            "short": "Move (register)",
        },
        {
            "instr": "VMOV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289964290.htm",
            "short": "Insert floating-point immediate in single-precision or double-precision register, or copy one FP register into another FP register of the same width",
        },
    ],
    "VMOVL": [
        {
            "instr": "VMOVL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289964290.htm",
            "short": "Move Long",
        }
    ],
    "VMOV{U}N": [
        {
            "instr": "VMOV{U}N",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289977128.htm",
            "short": "Move Narrow (register)",
        }
    ],
    "VMRS": [
        {
            "instr": "VMRS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433211144.htm",
            "short": "Transfer contents from a floating-point system register to an ARM register",
        }
    ],
    "VMSR": [
        {
            "instr": "VMSR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424868721235.htm",
            "short": "Transfer contents from an ARM register to a floating-point system register",
        }
    ],
    "VMUL": [
        {
            "instr": "VMUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Multiply (vector)",
        },
        {
            "instr": "VMUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Multiply (by scalar)",
        },
        {
            "instr": "VMUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Multiply",
        },
    ],
    "VMVN": [
        {
            "instr": "VMVN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289964640.htm",
            "short": "Move Negative (immediate)",
        }
    ],
    "VNEG": [
        {
            "instr": "VNEG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289968850.htm",
            "short": "Negate",
        },
        {
            "instr": "VNEG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289968850.htm",
            "short": "Negate",
        },
    ],
    "VNMLA": [
        {
            "instr": "VNMLA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289958611.htm",
            "short": "Negated multiply accumulate",
        }
    ],
    "VNMLS": [
        {
            "instr": "VNMLS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289960701.htm",
            "short": "Negated multiply subtract",
        }
    ],
    "VNMUL": [
        {
            "instr": "VNMUL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Negated multiply",
        }
    ],
    "VORN": [
        {
            "instr": "VORN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289952722.htm",
            "short": "Bitwise OR NOT",
        },
        {
            "instr": "VORN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289952722.htm",
            "short": "Bitwise OR NOT (pseudo-instruction)",
        },
    ],
    "VORR": [
        {
            "instr": "VORR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898123112.htm",
            "short": "Bitwise OR (register)",
        },
        {
            "instr": "VORR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425898123112.htm",
            "short": "Bitwise OR (immediate)",
        },
    ],
    "VPADAL": [
        {
            "instr": "VPADAL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289972209.htm",
            "short": "Pairwise Add and Accumulate",
        }
    ],
    "VPADD": [
        {
            "instr": "VPADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289973079.htm",
            "short": "Pairwise Add",
        }
    ],
    "VPMAX": [
        {
            "instr": "VPMAX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289974299.htm",
            "short": "Pairwise Maximum",
        }
    ],
    "VPMIN": [
        {
            "instr": "VPMIN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289974299.htm",
            "short": "Pairwise Minimum",
        }
    ],
    "VPOP": [
        {
            "instr": "VPOP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289974629.htm",
            "short": "Extension register load multiple",
        }
    ],
    "VPUSH": [
        {
            "instr": "VPUSH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289974949.htm",
            "short": "Extension register store multiple",
        }
    ],
    "VQABS": [
        {
            "instr": "VQABS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289975389.htm",
            "short": "Absolute value, saturate",
        }
    ],
    "VQADD": [
        {
            "instr": "VQADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289975719.htm",
            "short": "Add, saturate",
        }
    ],
    "VQDMLAL": [
        {
            "instr": "VQDMLAL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289959991.htm",
            "short": "Saturating Doubling Multiply Accumulate",
        }
    ],
    "VQDMLSL": [
        {
            "instr": "VQDMLSL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289961391.htm",
            "short": "Saturating Doubling Multiply Subtract",
        }
    ],
    "VQDMULH": [
        {
            "instr": "VQDMULH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Saturating Doubling Multiply returning High half",
        }
    ],
    "VQDMULL": [
        {
            "instr": "VQDMULL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289967170.htm",
            "short": "Saturating Doubling Multiply",
        }
    ],
    "VQMOV{U}N": [
        {
            "instr": "VQMOV{U}N",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289977128.htm",
            "short": "Saturating Move (register)",
        }
    ],
    "VQNEG": [
        {
            "instr": "VQNEG",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289977458.htm",
            "short": "Negate, saturate",
        }
    ],
    "VQRDMULH": [
        {
            "instr": "VQRDMULH",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289966080.htm",
            "short": "Saturating Doubling Multiply returning High half",
        }
    ],
    "VQRSHL": [
        {
            "instr": "VQRSHL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289983597.htm",
            "short": "Shift Left, Round, saturate (by signed variable)",
        }
    ],
    "VQRSHR{U}N": [
        {
            "instr": "VQRSHR{U}N",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289984317.htm",
            "short": "Shift Right, Round, saturate (by immediate)",
        }
    ],
    "VQSHL": [
        {
            "instr": "VQSHL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289944294.htm",
            "short": "Shift Left, saturate (by immediate)",
        },
        {
            "instr": "VQSHL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289944294.htm",
            "short": "Shift Left, saturate (by signed variable)",
        },
    ],
    "VQSHR{U}N": [
        {
            "instr": "VQSHR{U}N",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289979988.htm",
            "short": "Shift Right, saturate (by immediate)",
        }
    ],
    "VQSUB": [
        {
            "instr": "VQSUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289979988.htm",
            "short": "Subtract, saturate",
        }
    ],
    "VRADDHN": [
        {
            "instr": "VRADDHN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289980388.htm",
            "short": "Add, select High half, Round",
        }
    ],
    "VRECPE": [
        {
            "instr": "VRECPE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289980708.htm",
            "short": "Reciprocal Estimate",
        }
    ],
    "VRECPS": [
        {
            "instr": "VRECPS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289981068.htm",
            "short": "Reciprocal Step",
        }
    ],
    "VREV": [
        {
            "instr": "VREV",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425901506568.htm",
            "short": "Reverse elements",
        }
    ],
    "VRHADD": [
        {
            "instr": "VRHADD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289981768.htm",
            "short": "Halving Add, Round",
        }
    ],
    "VRINT": [
        {
            "instr": "VRINT",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433211604.htm",
            "short": "Round to integer",
        }
    ],
    "VRSHR": [
        {
            "instr": "VRSHR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433211144.htm",
            "short": "Shift Right and Round (by immediate)",
        }
    ],
    "VRSHRN": [
        {
            "instr": "VRSHRN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289984317.htm",
            "short": "Shift Right, Round, Narrow (by immediate)",
        }
    ],
    "VRSQRTE": [
        {
            "instr": "VRSQRTE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289983217.htm",
            "short": "Reciprocal Square Root Estimate",
        }
    ],
    "VRSQRTS": [
        {
            "instr": "VRSQRTS",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289983597.htm",
            "short": "Reciprocal Square Root Step",
        }
    ],
    "VRSRA": [
        {
            "instr": "VRSRA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424433211144.htm",
            "short": "Shift Right, Round, and Accumulate (by immediate)",
        }
    ],
    "VRSUBHN": [
        {
            "instr": "VRSUBHN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289984317.htm",
            "short": "Subtract, select High half, Round",
        }
    ],
    "VSHL": [
        {
            "instr": "VSHL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289944294.htm",
            "short": "Shift Left (by immediate)",
        }
    ],
    "VSHR": [
        {
            "instr": "VSHR",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424868721235.htm",
            "short": "Shift Right (by immediate)",
        }
    ],
    "VSHRN": [
        {
            "instr": "VSHRN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289992406.htm",
            "short": "Shift Right, Narrow (by immediate)",
        }
    ],
    "VSLI": [
        {
            "instr": "VSLI",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289987667.htm",
            "short": "Shift Left and Insert",
        }
    ],
    "VSRA": [
        {
            "instr": "VSRA",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1424868721235.htm",
            "short": "Shift Right, Accumulate (by immediate)",
        }
    ],
    "VSRI": [
        {
            "instr": "VSRI",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289989376.htm",
            "short": "Shift Right and Insert",
        }
    ],
    "VST": [
        {
            "instr": "VST",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289989776.htm",
            "short": "Vector Store",
        }
    ],
    "VSUB": [
        {
            "instr": "VSUB",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289992056.htm",
            "short": "Subtract",
        }
    ],
    "VSUBHN": [
        {
            "instr": "VSUBHN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289992406.htm",
            "short": "Subtract, select High half",
        }
    ],
    "VSWP": [
        {
            "instr": "VSWP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289993116.htm",
            "short": "Swap vectors",
        }
    ],
    "VTBL": [
        {
            "instr": "VTBL",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289993506.htm",
            "short": "Vector table look-up",
        }
    ],
    "VTBX": [
        {
            "instr": "VTBX",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289993506.htm",
            "short": "Vector table look-up",
        }
    ],
    "VTRN": [
        {
            "instr": "VTRN",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289994926.htm",
            "short": "Vector transpose",
        }
    ],
    "VTST": [
        {
            "instr": "VTST",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289995306.htm",
            "short": "Test bits",
        }
    ],
    "VUZP": [
        {
            "instr": "VUZP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289995635.htm",
            "short": "Vector de-interleave",
        }
    ],
    "VZIP": [
        {
            "instr": "VZIP",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_dom1361289996005.htm",
            "short": "Vector interleave",
        }
    ],
    "WFE": [
        {
            "instr": "WFE",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917119639.htm",
            "short": "Wait For Event",
        }
    ],
    "WFI": [
        {
            "instr": "WFI",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917144829.htm",
            "short": "Wait For Interrupt",
        }
    ],
    "YIELD": [
        {
            "instr": "YIELD",
            "link": "http://www.keil.com/support/man/docs/armclang_asm/armclang_asm_pge1425917160673.htm",
            "short": "Yield",
        }
    ],
}

reg = re.compile("B[LNEG][ETQ]")


def find_proper_name(instruction):
    out = str(instruction).strip().upper()
    if reg.match(out):
        return "B"
    return out


def get_doc_url(i):
    """ Takes in the instruction tokens and returns [(short form, doc url)] """
    names = map(find_proper_name, i)  # handles instruction prefixes
    output = []
    for name in names:
        if name in instrs.keys():
            inst_l = instrs[name]
            for inst_data in inst_l:
                output.append((inst_data["short"], inst_data["link"]))
    if len(output) == 0:
        return [
            (
                "No documentation for that instruction!",
                "https://github.com/ehennenfent/binja_explain_instruction/blob/master/CONTRIBUTING.md",
            )
        ]
    return output
