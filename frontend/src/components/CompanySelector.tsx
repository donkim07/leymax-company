import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Button,
  Menu,
  MenuItem,
  Typography,
  Avatar,
  Divider,
} from '@mui/material';
import { KeyboardArrowDown } from '@mui/icons-material';
import { selectUser } from '../store/slices/authSlice';
import { setCurrentModule } from '../store/slices/uiSlice';

const CompanySelector = () => {
  const dispatch = useDispatch();
  const user = useSelector(selectUser);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [companies, setCompanies] = useState<Array<{
    id: number;
    name: string;
    type: 'bakery' | 'tools' | 'academy';
    logo_url?: string;
  }>>([]);
  const [selectedCompany, setSelectedCompany] = useState<{
    id: number;
    name: string;
    type: 'bakery' | 'tools' | 'academy';
    logo_url?: string;
  } | null>(null);

  // In a real implementation, fetch the user's companies from the API
  useEffect(() => {
    if (user) {
      // Mock data - replace with API call
      const mockCompanies = [
        { id: 1, name: 'Sweet Delights Bakery', type: 'bakery' as const, logo_url: '/logos/bakery.png' },
        { id: 2, name: 'Cake Tools Pro', type: 'tools' as const, logo_url: '/logos/tools.png' },
        { id: 3, name: 'Leymax Academy', type: 'academy' as const, logo_url: '/logos/academy.png' },
      ];
      setCompanies(mockCompanies);
      setSelectedCompany(mockCompanies[0]);
      dispatch(setCurrentModule(mockCompanies[0].type));
    }
  }, [user, dispatch]);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleCompanySelect = (company: typeof selectedCompany) => {
    setSelectedCompany(company);
    dispatch(setCurrentModule(company?.type || null));
    handleClose();
  };

  if (!selectedCompany) return null;

  const getCompanyColor = (type: 'bakery' | 'tools' | 'academy') => {
    switch (type) {
      case 'bakery':
        return '#CF52DF';
      case 'tools':
        return '#9b51e0';
      case 'academy':
        return '#0F172A';
      default:
        return '#CF52DF';
    }
  };

  return (
    <Box>
      <Button
        onClick={handleClick}
        sx={{
          display: 'flex',
          alignItems: 'center',
          textTransform: 'none',
          color: getCompanyColor(selectedCompany.type),
          fontWeight: 600,
        }}
        endIcon={<KeyboardArrowDown />}
      >
        <Avatar
          src={selectedCompany.logo_url}
          sx={{ 
            width: 32, 
            height: 32, 
            mr: 1,
            bgcolor: getCompanyColor(selectedCompany.type)
          }}
        >
          {selectedCompany.name.charAt(0)}
        </Avatar>
        <Typography variant="subtitle1">{selectedCompany.name}</Typography>
      </Button>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        PaperProps={{
          elevation: 3,
          sx: { width: 250, maxWidth: '100%' },
        }}
      >
        <Typography variant="subtitle2" sx={{ px: 2, py: 1, fontWeight: 600 }}>
          Your Companies
        </Typography>
        <Divider />
        {companies.map((company) => (
          <MenuItem
            key={company.id}
            onClick={() => handleCompanySelect(company)}
            selected={selectedCompany?.id === company.id}
            sx={{ py: 1.5 }}
          >
            <Avatar
              src={company.logo_url}
              sx={{ 
                width: 32, 
                height: 32, 
                mr: 2,
                bgcolor: getCompanyColor(company.type)
              }}
            >
              {company.name.charAt(0)}
            </Avatar>
            <Box>
              <Typography variant="body1">{company.name}</Typography>
              <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'capitalize' }}>
                {company.type}
              </Typography>
            </Box>
          </MenuItem>
        ))}
      </Menu>
    </Box>
  );
};

export default CompanySelector; 