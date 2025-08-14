import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, Mail, Send, Inbox, Archive, Clock, User, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback } from '../components/ui/avatar';
import { Input } from '../components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { useToast } from '../hooks/use-toast';
import axios from 'axios';

const Emails = () => {
  const { toast } = useToast();
  const [emails, setEmails] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('inbox');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 10,
    total: 0,
    pages: 0
  });

  useEffect(() => {
    fetchEmails();
    fetchTemplates();
  }, [pagination.page, statusFilter, activeTab]);

  const fetchEmails = async () => {
    try {
      setLoading(true);
      
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        ...(searchTerm && { search: searchTerm }),
        ...(statusFilter !== 'all' && { status: statusFilter }),
        direction: activeTab === 'sent' ? 'outbound' : activeTab === 'inbox' ? 'inbound' : undefined
      };

      const response = await axios.get('/emails', { params });
      
      setEmails(response.data.emails);
      setPagination(prev => ({
        ...prev,
        total: response.data.total,
        pages: response.data.pages
      }));

    } catch (error) {
      console.error('Failed to fetch emails:', error);
      toast({
        title: "Error",
        description: "Failed to load emails. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await axios.get('/emails/templates');
      setTemplates(response.data.templates);
    } catch (error) {
      console.error('Failed to fetch templates:', error);
    }
  };

  const handleSearch = () => {
    setPagination(prev => ({ ...prev, page: 1 }));
    fetchEmails();
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'sent':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
      case 'delivered':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'read':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400';
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
      case 'draft':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getTabIcon = (tab) => {
    switch (tab) {
      case 'inbox':
        return <Inbox className="h-4 w-4" />;
      case 'sent':
        return <Send className="h-4 w-4" />;
      case 'templates':
        return <Archive className="h-4 w-4" />;
      default:
        return <Mail className="h-4 w-4" />;
    }
  };

  return (
    <div className="p-6 space-y-6 bg-gray-50 dark:bg-gray-900/50 min-h-screen">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Email Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage email communications with leads and clients
          </p>
        </div>
        <Button className="bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700 text-black font-semibold shadow-lg shadow-yellow-500/25">
          <Plus className="h-4 w-4 mr-2" />
          Compose Email
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-blue-100 dark:bg-blue-900/30 p-2 rounded-full">
                <Mail className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Emails</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{pagination.total}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-green-100 dark:bg-green-900/30 p-2 rounded-full">
                <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Delivered</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {emails.filter(email => email.status === 'delivered').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-full">
                <Archive className="h-5 w-5 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Templates</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{templates.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-yellow-100 dark:bg-yellow-900/30 p-2 rounded-full">
                <Clock className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">This Week</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {emails.filter(email => {
                    const emailDate = new Date(email.created_at);
                    const weekAgo = new Date();
                    weekAgo.setDate(weekAgo.getDate() - 7);
                    return emailDate >= weekAgo;
                  }).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs and Filters */}
      <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
        <CardContent className="p-6">
          {/* Tab Navigation */}
          <div className="flex gap-1 mb-4 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg w-fit">
            {['inbox', 'sent', 'templates'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === tab
                    ? 'bg-white dark:bg-gray-800 text-yellow-600 dark:text-yellow-400 shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                {getTabIcon(tab)}
                <span className="capitalize">{tab}</span>
              </button>
            ))}
          </div>

          {/* Search and Filters */}
          <div className="flex gap-4 items-center">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search emails by subject, sender, or content..."
                className="pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="sent">Sent</SelectItem>
                <SelectItem value="delivered">Delivered</SelectItem>
                <SelectItem value="read">Read</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
                <SelectItem value="draft">Draft</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={handleSearch} variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              Search
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Content Area */}
      <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-gray-700">
        <CardHeader>
          <CardTitle className="text-gray-900 dark:text-white capitalize">{activeTab}</CardTitle>
        </CardHeader>
        <CardContent>
          {activeTab === 'templates' ? (
            // Templates View
            <div className="space-y-4">
              {templates.length === 0 ? (
                <div className="text-center py-8">
                  <Archive className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 dark:text-gray-400">No email templates found</p>
                </div>
              ) : (
                templates.map((template) => (
                  <div
                    key={template.id}
                    className="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-full">
                        <Archive className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">{template.name}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{template.subject}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <Badge className="bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400">
                        {template.templateType || template.template_type}
                      </Badge>
                      <Button variant="outline" size="sm">
                        Use Template
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </div>
          ) : (
            // Emails View
            loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500 mx-auto"></div>
                <p className="text-gray-600 dark:text-gray-400 mt-2">Loading emails...</p>
              </div>
            ) : emails.length === 0 ? (
              <div className="text-center py-8">
                <Mail className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 dark:text-gray-400">No emails found</p>
              </div>
            ) : (
              <div className="space-y-4">
                {emails.map((email) => (
                  <div
                    key={email.id}
                    className="flex items-center justify-between p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <Avatar className="h-10 w-10">
                        <AvatarFallback className="bg-gradient-to-br from-yellow-500 to-yellow-600 text-black font-semibold">
                          {email.direction === 'inbound' ? 
                            email.lead_name?.split(' ').map(n => n[0]).join('') || 'L' :
                            email.agent_name?.split(' ').map(n => n[0]).join('') || 'A'
                          }
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold text-gray-900 dark:text-white">{email.subject}</h3>
                          <Badge className={getStatusColor(email.status)}>
                            {email.status?.toUpperCase()}
                          </Badge>
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {email.direction === 'inbound' ? `From: ${email.lead_name}` : `To: ${email.lead_name}`}
                          </span>
                          <span>{email.direction === 'inbound' ? email.from_email : email.to_email}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <p className="text-sm text-gray-900 dark:text-white">
                        {formatDate(email.created_at)}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {email.agent_name}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )
          )}
          
          {/* Pagination - Only show for emails, not templates */}
          {activeTab !== 'templates' && pagination.pages > 1 && (
            <div className="flex items-center justify-between mt-6">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Showing {((pagination.page - 1) * pagination.limit) + 1} to {Math.min(pagination.page * pagination.limit, pagination.total)} of {pagination.total} emails
              </p>
              
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                  disabled={pagination.page === 1}
                >
                  Previous
                </Button>
                
                <div className="flex gap-1">
                  {Array.from({ length: Math.min(pagination.pages, 5) }, (_, i) => {
                    const pageNum = i + 1;
                    return (
                      <Button
                        key={pageNum}
                        variant={pagination.page === pageNum ? "default" : "outline"}
                        size="sm"
                        onClick={() => setPagination(prev => ({ ...prev, page: pageNum }))}
                      >
                        {pageNum}
                      </Button>
                    );
                  })}
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                  disabled={pagination.page === pagination.pages}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Emails;