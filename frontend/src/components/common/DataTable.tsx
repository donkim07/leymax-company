import React, { useState } from 'react';
import {
    Box,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TablePagination,
    TableRow,
    TableSortLabel,
    Paper,
    IconButton,
    Tooltip,
    TextField,
    InputAdornment,
} from '@mui/material';
import {
    Search as SearchIcon,
    FilterList as FilterListIcon,
} from '@mui/icons-material';

interface Column {
    id: string;
    label: string;
    minWidth?: number;
    align?: 'right' | 'left' | 'center';
    format?: (value: any) => string;
}

interface DataTableProps {
    columns: Column[];
    rows: any[];
    onRowClick?: (row: any) => void;
    actions?: React.ReactNode;
    defaultSortBy?: string;
    defaultSortDirection?: 'asc' | 'desc';
}

const DataTable: React.FC<DataTableProps> = ({
    columns,
    rows,
    onRowClick,
    actions,
    defaultSortBy,
    defaultSortDirection = 'asc',
}) => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [searchQuery, setSearchQuery] = useState('');
    const [orderBy, setOrderBy] = useState<string>(defaultSortBy || columns[0].id);
    const [orderDirection, setOrderDirection] = useState<'asc' | 'desc'>(defaultSortDirection);

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const handleSort = (columnId: string) => {
        const isAsc = orderBy === columnId && orderDirection === 'asc';
        setOrderDirection(isAsc ? 'desc' : 'asc');
        setOrderBy(columnId);
    };

    const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
        setPage(0);
    };

    const filteredRows = rows.filter((row) =>
        Object.values(row).some((value) =>
            value?.toString().toLowerCase().includes(searchQuery.toLowerCase())
        )
    );

    const sortedRows = filteredRows.sort((a, b) => {
        if (a[orderBy] < b[orderBy]) return orderDirection === 'asc' ? -1 : 1;
        if (a[orderBy] > b[orderBy]) return orderDirection === 'asc' ? 1 : -1;
        return 0;
    });

    const paginatedRows = sortedRows.slice(
        page * rowsPerPage,
        page * rowsPerPage + rowsPerPage
    );

    return (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
            <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
                <TextField
                    size="small"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={handleSearch}
                    sx={{ flex: 1 }}
                    InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <SearchIcon />
                            </InputAdornment>
                        ),
                    }}
                />
                <Tooltip title="Filter list">
                    <IconButton>
                        <FilterListIcon />
                    </IconButton>
                </Tooltip>
                {actions}
            </Box>
            <TableContainer sx={{ maxHeight: 440 }}>
                <Table stickyHeader>
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell
                                    key={column.id}
                                    align={column.align}
                                    style={{ minWidth: column.minWidth }}
                                >
                                    <TableSortLabel
                                        active={orderBy === column.id}
                                        direction={orderBy === column.id ? orderDirection : 'asc'}
                                        onClick={() => handleSort(column.id)}
                                    >
                                        {column.label}
                                    </TableSortLabel>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {paginatedRows.map((row, index) => (
                            <TableRow
                                hover
                                role="checkbox"
                                tabIndex={-1}
                                key={index}
                                onClick={() => onRowClick?.(row)}
                                sx={{ cursor: onRowClick ? 'pointer' : 'default' }}
                            >
                                {columns.map((column) => {
                                    const value = row[column.id];
                                    return (
                                        <TableCell key={column.id} align={column.align}>
                                            {column.format ? column.format(value) : value}
                                        </TableCell>
                                    );
                                })}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={filteredRows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </Paper>
    );
};

export default DataTable;
