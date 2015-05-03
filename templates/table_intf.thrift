:: # Tenjin template file for table APIs for AIR_IRI

# Use JSON as a serialization format for maps and just use
# strings for thrift now.

# Not yet clear how much of this needs to be generated specific to
# the switch. May just generated helper functions that code/decode
# the structures based on the table definitions.

namespace py ${switch_prefix}_rpc

service ${switch_prefix} {

  # Generic calls with table as a parameter
  i32 table_entry_add(1:string table, 2:string matches, 3:string masks, 4:string action_name, 5:string action_params);
  i32 table_entry_delete(1:i32 entry_ref);

:: for name, val in air.table.items():
  # Interfaces for table ${name}
  i32 table_${name}_entry_add(1:string matches, 2:string masks, 3:string action_name, 4:string action_params);
  i32 table_${name}_entry_delete(1:i32 entry_ref);

:: #end
}
