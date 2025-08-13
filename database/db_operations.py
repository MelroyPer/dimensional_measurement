from .db_connection import connect 

def retrieve(part_number: str = None, inspection_parameter: str = None):
    try:
        conn = connect()
        cursor = conn.cursor()

        # Base query
        query = """
        SELECT * FROM parts_master p
        INNER JOIN measurement_master m ON p.part_number = m.part_number
        """
        params = []

        # Add WHERE conditions based on provided arguments
        conditions = []
        if part_number:
            conditions.append("p.part_number = ?")
            params.append(part_number)
        if inspection_parameter:
            conditions.append("m.inspection_parameter = ?")
            params.append(inspection_parameter)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)

        # Fetch column names and rows
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return results

    finally:
        conn.close()

def insert_measurement_row(
    part_id_number, measurement_id, part_number, poka_yoke_biq, status,
    actual_value, inspection_date, shift_name, shift_incharge, image_path,
    recall_flag, recall_reason, recall_date, update_date, update_by
):
    try:
        conn = connect()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO qc_parameters_txn (
            part_id_number, measurement_id, part_number, poka_yoke_biq, status,
            actual_value, inspection_date, shift_name, shift_incharge, image_path,
            recall_flag, recall_reason, recall_date, update_date, update_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            part_id_number, measurement_id, part_number, poka_yoke_biq, status,
            actual_value, inspection_date, shift_name, shift_incharge, image_path,
            recall_flag, recall_reason, recall_date, update_date, update_by
        )
        
        cursor.execute(query, values)
        conn.commit()
        print("Row inserted successfully.")
        
    finally:
        conn.close()
